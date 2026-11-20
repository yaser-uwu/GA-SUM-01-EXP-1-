# Consulta de turnos del RTV mediante REST

**Kevin Leonel García Bazurto — EXP-1**

En este avance se preparó un cliente externo para consultar turnos del sistema de Revisión Técnica Vehicular. El cliente inicia sesión, envía una petición GET y muestra la respuesta del backend en JSON. La información se obtiene de la base PostgreSQL del RTV.

La consulta sirve para que el solicitante revise el estado y las fechas de su turno desde otra aplicación. El backend comprueba que el turno corresponda al propietario vinculado con la cuenta que inició sesión. Cambiar el identificador en la petición no permite consultar el turno de otra persona.

## Qué se hizo

Se añadió la ruta `GET /api/consulta/turnos/{id}` y la relación entre la cuenta del usuario y el propietario. También se separó el acceso del solicitante del acceso del personal, que conserva las consultas internas según sus permisos.

La respuesta del solicitante incluye cuatro datos: `turnoId`, `estado`, `fechaInicio` y `fechaFin`. Para comprobar el funcionamiento se prepararon una cuenta, un propietario y un turno ficticios, y se hicieron consultas con y sin autorización.

## Resultado de las pruebas

| Caso | Respuesta |
|---|---|
| Consultar el turno propio | `200`, con los datos del turno. |
| Consultar un turno ajeno o inexistente | `404`, sin mostrar sus datos. |
| Consultar sin iniciar sesión | `401`. |
| Intentar el listado del personal con la cuenta del solicitante | `403`. |
| Consultar con una cuenta del personal autorizada | `200`. |

También pasaron las diez pruebas automatizadas del backend, sin fallos ni errores.

## Archivos de este aporte

- `index.html` y `ClienteConsulta.java`: cliente web y cliente Java.
- `backend-consulta-turnos.patch`: cambios realizados en el backend del RTV, incluida la tabla de vinculación y las pruebas.
- `peticiones.http`, `respuesta-200.http` y `respuesta-404.http`: peticiones y respuestas de la consulta.
- `turno-propio-200.jpg` y `turno-ajeno-404.jpg`: capturas de las pruebas.
- `resultado-pruebas.txt`: resultado de las pruebas automatizadas.
- [Guía de prueba](GUIA-DE-PRUEBA.md): pasos para probarlo con el RTV y aspectos que deben adaptarse para utilizar otro proyecto.

## Relación con la propuesta

La demo muestra el cliente externo y la consulta autorizada sobre el backend actual. En el [diagrama](../../diagramas/kevin-rest.drawio) se propone separar el servicio de consulta y utilizar una base de lectura actualizada mediante eventos. Esa separación corresponde a una siguiente etapa de la propuesta.

## Apoyo de inteligencia artificial

Se utilizó ChatGPT Sol 6.1 en su forma Codex como apoyo para preparar el cliente, los cambios del backend, las pruebas y la documentación.
