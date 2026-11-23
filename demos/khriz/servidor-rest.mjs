// Prototipo de EXP-1: datos ficticios, sin conexión al backend ni a la BD de SGRA.
import { createServer } from 'node:http';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const RUTA = '/api/student/requests';
const MAX_BYTES = 16 * 1024;

function responder(response, status, body, headers = {}) {
  response.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    ...headers,
  });
  response.end(JSON.stringify(body));
}

async function leerJson(request) {
  const chunks = [];
  let bytes = 0;
  for await (const chunk of request) {
    bytes += chunk.length;
    if (bytes <= MAX_BYTES) chunks.push(chunk);
  }
  if (bytes > MAX_BYTES) {
    const error = new Error('El cuerpo supera 16 KiB.');
    error.status = 413;
    throw error;
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}

function validar(datos) {
  if (!datos || typeof datos !== 'object' || Array.isArray(datos)) {
    return { body: 'Se requiere un objeto JSON.' };
  }
  const errors = {};
  if (!Number.isSafeInteger(datos.subjectId) || datos.subjectId <= 0) {
    errors.subjectId = 'Selecciona un identificador de asignatura entero y positivo.';
  }
  if (datos.sessionTypeId !== 1) {
    errors.sessionTypeId = 'Esta demo admite únicamente el tipo 1: Individual.';
  }
  if (typeof datos.reason !== 'string' || datos.reason.trim().length < 10) {
    errors.reason = 'El motivo es obligatorio y debe tener al menos 10 caracteres.';
  }
  if (typeof datos.preferredSchedule !== 'string' || !datos.preferredSchedule.trim()) {
    errors.preferredSchedule = 'Indica tu disponibilidad preferida.';
  }
  return errors;
}

export function crearServicio() {
  // El mapa permite comprobar que una petición inválida no crea registros.
  // No es persistencia duradera ni una implementación de idempotencia.
  const solicitudes = new Map();
  let siguienteId = 1;
  const server = createServer(async (request, response) => {
    if (request.url !== RUTA) {
      responder(response, 404, { error: 'Ruta no encontrada.' });
      return;
    }
    if (request.method !== 'POST') {
      responder(response, 405, { error: 'Utiliza POST para crear una solicitud.' }, { Allow: 'POST' });
      return;
    }
    const tipo = request.headers['content-type']?.split(';')[0].trim().toLowerCase();
    if (tipo !== 'application/json') {
      responder(response, 415, { error: 'Utiliza Content-Type: application/json.' });
      return;
    }
    try {
      const datos = await leerJson(request);
      const errors = validar(datos);
      if (Object.keys(errors).length) {
        responder(response, 400, { error: 'Solicitud inválida.', fields: errors });
        return;
      }
      const requestId = siguienteId++;
      solicitudes.set(requestId, {
        requestId,
        // Identidad de escenario fijada en el servidor; no representa una sesión real.
        studentId: 1,
        subjectId: datos.subjectId,
        sessionTypeId: datos.sessionTypeId,
        reason: datos.reason.trim(),
        preferredSchedule: datos.preferredSchedule.trim(),
        status: 'Pendiente',
      });
      responder(response, 201, { requestId });
    } catch (error) {
      if (error instanceof SyntaxError) {
        responder(response, 400, { error: 'JSON mal formado.' });
      } else if (error.status === 413) {
        responder(response, 413, { error: error.message });
      } else {
        responder(response, 500, { error: 'No se pudo procesar la solicitud.' });
      }
    }
  });
  server.requestTimeout = 15_000;
  server.headersTimeout = 10_000;
  return { server, solicitudes };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const port = Number(process.env.PORT ?? 8083);
  if (!Number.isInteger(port) || port < 0 || port > 65535) {
    console.error('PORT debe ser un entero entre 0 y 65535.');
    process.exitCode = 1;
  } else {
    const { server } = crearServicio();
    server.on('error', (error) => {
      console.error('No se pudo iniciar la demo: ' + error.message);
      process.exitCode = 1;
    });
    server.listen(port, '127.0.0.1', () => {
      console.log('Demo SGRA: http://127.0.0.1:' + server.address().port + RUTA);
      console.log('POST con JSON. Datos ficticios y almacenamiento en memoria. Ctrl+C para detener.');
    });
    for (const signal of ['SIGINT', 'SIGTERM']) {
      process.once(signal, () => {
        server.close();
        server.closeIdleConnections?.();
      });
    }
  }
}
