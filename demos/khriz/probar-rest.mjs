import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { once } from 'node:events';
import { crearServicio } from './servidor-rest.mjs';

const valida = await readFile(new URL('./peticion-valida.json', import.meta.url), 'utf8');
const sinMotivo = await readFile(new URL('./peticion-sin-motivo.json', import.meta.url), 'utf8');
const { server, solicitudes } = crearServicio();
server.listen(0, '127.0.0.1');
await once(server, 'listening');
const endpoint = 'http://127.0.0.1:' + server.address().port + '/api/student/requests';
const lineas = ['Pruebas de EXP-1 / Khriz / prototipo SGRA',
  'Ejecución UTC: ' + new Date().toISOString(), 'Node.js: ' + process.version,
  'Servicio local temporal: ' + endpoint, 'Datos ficticios; registros en memoria.', ''];

async function enviar(body, contentType = 'application/json') {
  const response = await fetch(endpoint, {
    method: 'POST', headers: { 'Content-Type': contentType }, body,
    signal: AbortSignal.timeout(5000),
  });
  return { response, body: await response.text() };
}

async function conservar(nombre, payload, resultado) {
  if (!process.argv.includes('--guardar-evidencias')) return;
  const url = new URL(endpoint);
  await writeFile(new URL('./peticion-' + nombre + '.http', import.meta.url),
    'POST ' + endpoint + ' HTTP/1.1\nHost: ' + url.host +
    '\nContent-Type: application/json\n\n' + payload.trim() + '\n');
  const headers = [...resultado.response.headers].map(([k, v]) => k + ': ' + v).join('\n');
  await writeFile(new URL('./respuesta-' + nombre + '.http', import.meta.url),
    'HTTP/1.1 ' + resultado.response.status + ' ' + resultado.response.statusText +
    '\n' + headers + '\n\n' + resultado.body + '\n');
}

function aprobado(mensaje) { lineas.push('OK - ' + mensaje); console.log('OK - ' + mensaje); }

try {
  const creada = await enviar(valida);
  assert.equal(creada.response.status, 201);
  assert.deepEqual(JSON.parse(creada.body), { requestId: 1 });
  assert.match(creada.response.headers.get('content-type'), /application\/json/);
  assert.equal(solicitudes.size, 1);
  assert.equal(solicitudes.get(1).status, 'Pendiente');
  assert.equal(solicitudes.get(1).preferredSchedule, JSON.parse(valida).preferredSchedule);
  await conservar('valida', valida, creada);
  aprobado('Solicitud válida: HTTP 201, identificador 1 y registro Pendiente.');

  const invalida = await enviar(sinMotivo);
  assert.equal(invalida.response.status, 400);
  assert.ok(JSON.parse(invalida.body).fields.reason);
  assert.equal(solicitudes.size, 1);
  await conservar('sin-motivo', sinMotivo, invalida);
  aprobado('Sin motivo: HTTP 400 y ningún registro adicional.');

  const malformada = await enviar('{"subjectId":');
  assert.equal(malformada.response.status, 400);
  assert.deepEqual(JSON.parse(malformada.body), { error: 'JSON mal formado.' });
  assert.equal(solicitudes.size, 1);
  await conservar('json-invalido', '{"subjectId":', malformada);
  aprobado('JSON mal formado: HTTP 400 sin detener el servicio.');

  const casos = [
    ['Disponibilidad ausente', { ...JSON.parse(valida), preferredSchedule: '  ' }, 'preferredSchedule'],
    ['Motivo demasiado corto', { ...JSON.parse(valida), reason: '   corto   ' }, 'reason'],
    ['Identificador inválido', { ...JSON.parse(valida), subjectId: 0 }, 'subjectId'],
    ['Tipo grupal fuera del alcance', { ...JSON.parse(valida), sessionTypeId: 2 }, 'sessionTypeId'],
    ['Cuerpo que no es objeto', [], 'body'],
  ];
  for (const [label, payload, campo] of casos) {
    const resultado = await enviar(JSON.stringify(payload));
    assert.equal(resultado.response.status, 400);
    assert.ok(JSON.parse(resultado.body).fields[campo]);
    assert.equal(solicitudes.size, 1);
    aprobado(label + ': HTTP 400, sin insertar.');
  }

  const tipo = await enviar(valida, 'text/plain');
  assert.equal(tipo.response.status, 415);
  assert.equal(solicitudes.size, 1);
  aprobado('Tipo de contenido incorrecto: HTTP 415.');

  const grande = await enviar(JSON.stringify({ reason: 'x'.repeat(17 * 1024) }));
  assert.equal(grande.response.status, 413);
  assert.equal(solicitudes.size, 1);
  aprobado('Cuerpo mayor de 16 KiB: HTTP 413, sin insertar.');

  const metodo = await fetch(endpoint, { signal: AbortSignal.timeout(5000) });
  assert.equal(metodo.status, 405);
  assert.equal(metodo.headers.get('allow'), 'POST');
  await metodo.text();
  aprobado('GET en la ruta de creación: HTTP 405 y Allow: POST.');

  const posterior = await enviar(valida);
  assert.equal(posterior.response.status, 201);
  assert.deepEqual(JSON.parse(posterior.body), { requestId: 2 });
  assert.equal(solicitudes.size, 2);
  aprobado('Nueva solicitud tras errores: HTTP 201 e identificador 2.');

  lineas.push('', 'Resultado: 12 comprobaciones aprobadas.',
    'La repetición de una petición válida crea otro registro: la idempotencia es una propuesta.',
    'El servicio temporal se cierra al terminar. Los puertos de las evidencias no son permanentes.');
  if (process.argv.includes('--guardar-evidencias')) {
    await writeFile(new URL('./resultado-pruebas.txt', import.meta.url), lineas.join('\n') + '\n');
  }
  console.log('\n12 comprobaciones aprobadas.');
} finally {
  await new Promise((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve());
    server.closeIdleConnections?.();
  });
}
