# Validación SOAP de una reserva de laboratorio

Demostración local de la operación propuesta para CLAB. Usa el código de laboratorio, la fecha y las horas de inicio y fin que aparecen en el modelo de reserva del PFC, junto con un identificador ficticio de solicitud.

## Cómo repetir la prueba

Requiere Node.js 18 o posterior. Desde esta carpeta, ejecuta:

    node practica-soap.mjs

El programa levanta un servicio HTTP en 127.0.0.1, comprueba que el WSDL está accesible y envía dos solicitudes SOAP 1.1. Al terminar, cierra el servicio y la URL temporal deja de estar disponible.

| Caso | Petición | Resultado observado |
| --- | --- | --- |
| Reserva completa | peticion-valida.xml | HTTP 200 y acuse para RES-123 en respuesta-valida.xml |
| Reserva sin hora de fin | peticion-sin-hora-fin.xml | HTTP 500 y SOAP Fault en respuesta-sin-hora-fin.xml |

Para regenerar los cuatro XML desde la ejecución, usa:

    node practica-soap.mjs --guardar-xml

La [captura de la ejecución en VS Code](ejecucion-soap.png) muestra ambos resultados.

## Alcance

El servicio de práctica reconoce los dos mensajes de ejemplo. El WSDL documenta el contrato propuesto. La prueba se ejecuta con datos ficticios y comprueba el intercambio de mensajes. La integración con el PFC, la validación general contra el esquema y la comprobación de disponibilidad quedan fuera del prototipo.

Se usó OpenAI Codex (GPT-6) como apoyo para preparar el prototipo y el WSDL. Juliana ejecutó los dos casos en su computadora y conservó la captura de la salida.
