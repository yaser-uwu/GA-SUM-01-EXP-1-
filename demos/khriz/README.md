# SGRA: crear una solicitud de refuerzo con REST

**Khriz Alexander Coronel Gómez — EXP-1.** Prototipo autónomo basado en RF01 del Sistema de Gestión de Refuerzo Académico. Usa Node.js 18 o posterior y sus módulos incluidos, sin npm ni base de datos.

## Ejecutar y probar

Desde esta carpeta:

```powershell
node servidor-rest.mjs
```

El servicio escucha únicamente en `http://127.0.0.1:8083`. En otra terminal, desde la misma carpeta:

```powershell
curl.exe -i -H "Content-Type: application/json" --data-binary "@peticion-valida.json" http://127.0.0.1:8083/api/student/requests
curl.exe -i -H "Content-Type: application/json" --data-binary "@peticion-sin-motivo.json" http://127.0.0.1:8083/api/student/requests
```

La primera petición devuelve `201 Created` y `{"requestId":1}` al iniciar una instancia nueva. La segunda devuelve `400` e identifica `reason` como campo inválido. También se pueden abrir las peticiones en un cliente HTTP del IDE o enviarlas con Postman. `Ctrl+C` detiene el servicio. Si el puerto está ocupado, definir `$env:PORT = '8084'` antes de iniciarlo y ajustar la URL del cliente.

Para comprobarlo automáticamente:

```powershell
node probar-rest.mjs
```

Esta prueba abre su propio servicio en un puerto libre, comprueba 12 escenarios y lo cierra. No requiere tener abierta la instancia del puerto 8083. Para conservar las respuestas de una ejecución real:

```powershell
node probar-rest.mjs --guardar-evidencias
```

El parámetro actualiza las peticiones y respuestas `.http` de los tres casos principales y `resultado-pruebas.txt`. Sus puertos temporales y fechas identifican esa ejecución; no son direcciones permanentes. El archivo `peticiones.http` mantiene la URL del servicio manual.

## Contrato del prototipo

`POST /api/student/requests`, con `Content-Type: application/json`.

| Campo | Validación |
| --- | --- |
| `subjectId` | Número entero positivo y seguro. |
| `sessionTypeId` | `1`: solicitud individual. |
| `reason` | Texto con al menos 10 caracteres después de retirar espacios de los extremos. |
| `preferredSchedule` | Disponibilidad preferida, como texto no vacío. No confirma una sesión. |

Con datos válidos se crea un registro en memoria, con identificador creciente, estudiante ficticio 1 y estado `Pendiente`. Una petición inválida no guarda datos ni consume un identificador. JSON mal formado recibe `400`; tipo de contenido incorrecto, `415`; cuerpos mayores de 16 KiB, `413`; otro método en la ruta, `405`; otra ruta, `404`.

## Procedencia y alcance

- RF01: [requisitos actuales del PFC-SGRA](https://github.com/Yukisan-uwo/PFC-SGRA/blob/main/docs/secciones/06-requisitos.tex).
- [Backend anterior enlazado desde el PFC](https://github.com/BelindaTZ/SEG-INF-back-SGRA-Docker/blob/main/src/main/java/com/CLMTZ/Backend/controller/reinforcement/student/StudentRequestController.java): utiliza la misma ruta, recibe `multipart/form-data` y devuelve `200` con `requestId`. Esta demo tiene un contrato simplificado JSON y devuelve el `201` exigido por la ficha de EXP-1.
- `preferredSchedule` responde al RF01 reformulado del PFC; no forma parte del DTO de creación consultado en el backend anterior.
- Todos los datos son ficticios. No se autentica a una persona ni se comprueban matrícula, docente, período o existencia real de la asignatura. El identificador del estudiante se fija en el servicio de prueba y no se recibe del cliente.
- No hay PostgreSQL, persistencia después de reiniciar, adjuntos, solicitudes grupales ni llamadas al SGRA real. Crear una solicitud no asigna docente ni reserva un cupo en este prototipo.
- No se implementa idempotencia: repetir una petición válida crea otro registro. La propuesta consiste en conservar una clave por operación, asociada al solicitante, al contenido y al resultado; los reintentos de esa operación recuperarían el identificador original. Esa relación y el registro deberían guardarse atómicamente y sobrevivir a reinicios en una integración real.
- Los dos nodos, la replicación y la coordinación para confirmar un último cupo pertenecen a la evolución propuesta. La demo local no prueba CAP, PACELC ni fallos de una réplica.

## Material y pendientes personales

Las notas y las diapositivas contienen un turno previsto de tres minutos: 60 s para el caso y las transparencias, 45 s para el POST, 30 s para reintentos y 45 s para CAP/PACELC.

- Leer la fuente y revisar la captura anotada preparada con asistencia de Codex.
- Dibujar y fotografiar el bosquejo auténtico, con nombres y fecha, para el anexo grupal.
- Revisar y comprender el código; conservar enlaces a los commits propios reales.
- Coordinar y grabar el ensayo con todos los integrantes; comprobar su enlace en ventana privada y añadirlo al README raíz.
- Formular una pregunta crítica a otro equipo. Ejemplo de preparación: «Si su sistema guarda una operación y pierde la respuesta, ¿cómo distingue un reintento de una operación nueva?».
- Confirmar con el docente la adaptación de la actividad a los cuatro PFC.

Se utilizó OpenAI Codex para implementar el prototipo, preparar documentación, diagramas y notas, y ejecutar comprobaciones. Esto no acredita un ensayo, una lectura personal, un bosquejo manual ni commits realizados por Khriz.
