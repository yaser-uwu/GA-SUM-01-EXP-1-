# Demo SOAP de Joseph (local y ficticia)

Este ejemplo implementa un servidor SOAP **1.2** y su contrato WSDL para ilustrar la verificación externa de un título. **No está conectado al SSDC ni a SENESCYT**; `TEST-001`, `TEST-002` y todos los resultados son datos inventados para la exposición. Usa Python 3 y solo módulos de la biblioteca estándar.

## Ejecutar y capturar la evidencia

Abre PowerShell en la carpeta `demos/joseph/` del repositorio. Si ya hay algo escuchando en el puerto 8000, ciérralo para la demostración manual.

```powershell
Get-Date
hostname
whoami
py -3 probar.py
```

Si `py` no existe, usa `python probar.py`. Este comando levanta un servidor local temporal, consulta el WSDL y envía cuatro peticiones HTTP. En pantalla debe mostrar `HTTP 200 | VALIDO`, `HTTP 200 | NO_VALIDO`, `HTTP 500 | codigoRegistro es obligatorio.` y `espera de 1 s agotada`, además de `RESULTADO: 4 casos y WSDL comprobados`.

Toma **tu propia captura** de esa terminal: la fecha/hora, el equipo, el usuario y las respuestas deben verse en la misma imagen. Guárdala en `evidencias/joseph-ejecucion-soap.png`. El script guarda las respuestas XML y un resumen de la prueba en `demos/joseph/responses/`; comprueba su contenido antes de subirlos. Los XML de entrada están en `demos/joseph/requests/`.

## Mostrar el servidor y el WSDL por separado

En una terminal: `py -3 server.py`. En otra: abre `http://127.0.0.1:8000/wsdl` en el navegador. El endpoint SOAP es `http://127.0.0.1:8000/soap`; **abrirlo por GET no ejecuta una operación**. Para enviar solicitudes por POST se pueden importar el WSDL en SoapUI o los archivos de `requests/` en Postman usando `Content-Type: application/soap+xml; charset=utf-8`. El script `probar.py` hace ambas partes sin instalar clientes externos.

La respuesta `VALIDO` solo corresponde al código ficticio `TEST-001`; no demuestra la validez de un título real. El `SOAP Fault` modela una solicitud mal formada y la petición lenta comprueba el tiempo máximo de espera del cliente.
