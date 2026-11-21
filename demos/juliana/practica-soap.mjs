// Ejercicio local con dos mensajes SOAP 1.1 de datos ficticios.
// El servicio reconoce los dos formatos de este ejercicio, sin implementar
// un analizador SOAP general ni validación contra WSDL.
import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { createServer } from 'node:http';

const envelope = (body) =>
  '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" ' +
  'xmlns:v="urn:practica:reserva-laboratorio"><soap:Body>' +
  body + '</soap:Body></soap:Envelope>';

const wsdl = await readFile(new URL('./practica-soap.wsdl', import.meta.url), 'utf8');
const sampleEnd = '11:00:00';
const requestXml = (end) => envelope(
  '<v:ValidarReserva><v:idSolicitud>RES-123</v:idSolicitud>' +
  '<v:codLaboratorio>1</v:codLaboratorio><v:fechaReserva>2026-11-25</v:fechaReserva>' +
  '<v:horaInicio>10:00:00</v:horaInicio>' +
  (end ? '<v:horaFin>' + end + '</v:horaFin>' : '') +
  '</v:ValidarReserva>',
);

const server = createServer(async (request, response) => {
  if (request.method === 'GET' && request.url === '/validar?wsdl') {
    const endpoint = 'http://127.0.0.1:' + server.address().port + '/validar';
    response.writeHead(200, { 'Content-Type': 'text/xml; charset=utf-8' });
    response.end(wsdl.replace('http://127.0.0.1:8080/validar', endpoint));
    return;
  }
  if (request.method !== 'POST' || request.url !== '/validar') {
    response.writeHead(404).end();
    return;
  }
  request.setEncoding('utf8');
  let incoming = '';
  for await (const chunk of request) {
    incoming += chunk;
    if (incoming.length > 4096) {
      response.writeHead(413).end();
      return;
    }
  }

  const valid = incoming === requestXml(sampleEnd);
  const missingEnd = incoming === requestXml('');
  const faultReason = missingEnd
    ? 'El campo horaFin es obligatorio.'
    : 'Mensaje fuera de los casos de práctica.';
  const body = valid
    ? '<v:Acuse><v:idSolicitud>RES-123</v:idSolicitud>' +
      '<v:resultado>Datos validos</v:resultado></v:Acuse>'
    : '<soap:Fault><faultcode>soap:Client</faultcode><faultstring>' +
      faultReason + '</faultstring><detail><v:ErrorValidacion>' +
      '<v:mensaje>' + faultReason + '</v:mensaje>' +
      '</v:ErrorValidacion></detail></soap:Fault>';
  response.writeHead(valid ? 200 : 500, { 'Content-Type': 'text/xml; charset=utf-8' });
  response.end(envelope(body));
});

await new Promise((resolve, reject) => {
  server.once('error', reject);
  server.listen(0, '127.0.0.1', resolve);
});

try {
  const endpoint = 'http://127.0.0.1:' + server.address().port + '/validar';
  const contract = await fetch(endpoint + '?wsdl', { signal: AbortSignal.timeout(3000) });
  assert.equal(contract.status, 200);
  assert.ok((await contract.text()).includes('location="' + endpoint + '"'));
  console.log('WSDL disponible durante la prueba: ' + endpoint + '?wsdl');

  const cases = [
    { file: 'valida', label: 'Reserva completa', end: sampleEnd, status: 200, contains: '<v:Acuse>' },
    { file: 'sin-hora-fin', label: 'Reserva sin hora de fin', end: '', status: 500, contains: 'El campo horaFin es obligatorio.' },
  ];
  for (const example of cases) {
    const payload = requestXml(example.end);
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'text/xml; charset=utf-8',
        SOAPAction: '"urn:practica:reserva-laboratorio:ValidarReserva"',
      },
      body: payload,
      signal: AbortSignal.timeout(3000),
    });
    const body = await response.text();
    assert.equal(response.status, example.status);
    assert.ok(body.includes(example.contains));
    if (process.argv.includes('--guardar-xml')) {
      await writeFile(new URL('./peticion-' + example.file + '.xml', import.meta.url), payload + '\n');
      await writeFile(new URL('./respuesta-' + example.file + '.xml', import.meta.url), body + '\n');
    }
    console.log(example.label + ' — HTTP ' + response.status + '\n' + body + '\n');
  }
} finally {
  server.close();
}
