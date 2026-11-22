# Bitácora del equipo CCEG — EXP-1

## 2026-11-18 — Kevin Leonel García Bazurto

- **Presentes:** Kevin Leonel García Bazurto.
- **Realizado:** Se definió la consulta REST de turnos del sistema de Revisión Técnica Vehicular y se publicó el bosquejo a mano de la propuesta.
- **Problemas encontrados:** Había que diferenciar la consulta del solicitante de las funciones del personal.
- **Solución:** Se planteó una aplicación externa para consultar el turno, sin permitir el acceso a las funciones internas.
- **Uso de inteligencia artificial:** Se utilizó ChatGPT Sol 6.1 mediante Codex para preparar el diseño y apoyar la explicación del flujo.

## 2026-11-18 — Joseph Alexander Calderón Saltos

- **Presentes:** Joseph Alexander Calderón Saltos.
- **Realizado:** Publiqué la primera versión de mis notas sobre una posible verificación externa mediante SOAP. El borrador inicial utilizaba un escenario de consulta de cobertura médica, que después se ajustó al SSDC.
- **Problema y solución:** No existía una integración confirmada con un proveedor externo. Dejé identificado el escenario como una propuesta futura, con datos de prueba y un contrato WSDL por definir.
- **Evidencia:** Commit `4661675f`, en `notas/secciones/joseph.tex`.
- **Uso de IA:** Utilicé ChatGPT (OpenAI) como apoyo para organizar la estructura del código LaTeX de mis notas.

## 2026-11-19 — Joseph Alexander Calderón Saltos

- **Presentes:** Joseph Alexander Calderón Saltos.
- **Realizado:** Amplié las notas con ejemplos XML de solicitud y respuesta SOAP. Documenté el uso de un tiempo máximo de espera y el tratamiento de una conexión fallida.
- **Problema y solución:** Una demora podía confundirse con una respuesta negativa del proveedor. Aclaré que, si no llega una respuesta válida, la consulta queda sin completar. Los mensajes XML se identificaron como ejemplos ilustrativos.
- **Evidencia:** Commit `079e5cd6`, en `notas/secciones/joseph.tex`.
- **Uso de IA:** Utilicé ChatGPT (OpenAI) como apoyo para organizar las estructura de las tarea.

## 2026-11-20 — Kevin Leonel García Bazurto

- **Presentes:** Kevin Leonel García Bazurto.
- **Realizado:** Se publicaron el diagrama editable y su imagen, las notas y las diapositivas. Se preparó la demo REST con el backend y PostgreSQL del RTV. El turno propio devolvió 200 y el ajeno 404. Se conservaron las peticiones, respuestas y capturas. Se incorporó un artículo sobre evolución de API, su referencia exportada de Zotero y una captura anotada.
- **Problemas encontrados:** El solicitante necesitaba consultar solo los turnos del propietario vinculado con su cuenta. También había que separar lo implementado de la arquitectura futura.
- **Solución:** Se incorporó la comprobación del vínculo entre usuario, propietario y turno. La cola, el consumidor y la base de lectura se identificaron como parte de la propuesta.
- **Uso de inteligencia artificial:** Se utilizó ChatGPT Sol 6.1 mediante Codex para ayudarme y guiarme con la preparación de código, documentación y material de exposición, y para que me ayude a comprobar las respuestas de la demo y la compilación.

## 2026-11-20 — Joseph Alexander Calderón Saltos

- **Presentes:** Joseph Alexander Calderón Saltos.
- **Realizado:** Ajusté el escenario de mis notas al Sistema de Selección Docente: una posible consulta del registro de un título académico. Publiqué el diagrama editable, su imagen y mis diapositivas con el flujo, los mensajes XML y el manejo propuesto de errores.
- **Problema y solución:** El borrador anterior trataba sobre cobertura médica. Lo adapté al SSDC y aclaré que el proveedor externo era hipotético, que los valores eran ficticios y que la respuesta solo apoyaría la revisión manual del documento.
- **Evidencias:** Commits `3391cf8c`, `f4e1c715` y `c65f8027`; archivos en `notas/secciones/`, `diagramas/` y `aportes/`.
- **Uso de IA:** Utilicé ChatGPT (OpenAI) como apoyo para ajustar la estructura del código LaTeX de mis notas.

## 2026-11-21 — Kevin Leonel García Bazurto

- **Presentes:** Kevin Leonel García Bazurto.
- **Realizado:** Se revisó la rúbrica de EXP-1 y el material publicado. Se ajustó la explicación de la ruta REST y se añadió cómo la propuesta oculta el acceso a las bases y comunica los fallos o los datos desactualizados. Se comprobó la compilación de las notas y de las diapositivas de Kevin.
- **Problemas encontrados:** La ruta ilustrativa del diagrama podía confundirse con la ruta usada en la demo.
- **Solución:** Se aclaró que la demo consulta el turno 82 mediante `/api/consulta/turnos/82` y que el identificador 123 del diagrama es ilustrativo.
- **Uso de inteligencia artificial:** Se utilizó ChatGPT Sol 6.1 mediante Codex para revisar y ajustar las notas y darle un mejor diseño a las diapositivas.

## 2026-11-21 — Juliana Romina Emanuel Pino

- **Trabajo individual:** Validación SOAP en el sistema de reservas de laboratorios.
- **Realizado:** Se ejecutaron los casos de solicitud completa y solicitud sin hora de fin. Se conservaron el acuse HTTP 200, el SOAP Fault HTTP 500, sus XML y la captura de VS Code.
- **Problema y solución:** Las notas describían el campo de ejemplo estado. Se actualizaron con el resultado observado al omitir horaFin. Se comparó la validación de campos con la comprobación de horarios de Microsoft Places y se añadieron fuentes recientes.
- **Uso de IA:** OpenAI Codex (GPT-6) apoyó la revisión del prototipo, la preparación de material y la comprobación de las referencias. Juliana ejecutó la demo y guardó su captura.

## 2026-11-21 — Joseph Alexander Calderón Saltos

- **Presentes:** Joseph Alexander Calderón Saltos.
- **Realizado:** Incorporé la demo SOAP 1.2 local, su contrato WSDL, las peticiones XML, el programa de prueba y las instrucciones de ejecución. Actualicé mis diapositivas y notas con las referencias bibliográficas.
- **Verificación:** Ejecuté `py -3 probar.py` en mi equipo. Se comprobó el WSDL y cuatro casos: `TEST-001` devolvió `VALIDO` con HTTP 200; `TEST-002` devolvió `NO_VALIDO` con HTTP 200; la solicitud sin código devolvió un SOAP Fault con HTTP 500; y la consulta lenta agotó el tiempo de espera del cliente después de un segundo.
- **Evidencias:** Publiqué las respuestas XML y el resumen en `demos/joseph/responses/`, la captura `evidencias/joseph-ejecucion-soap.png` y el bosquejo manual `evidencias/joseph-bosquejo-soap.jpg`.
- **Referencias:** Incorporé la referencia de Ayfan et al. (2024). Para explicar el contrato SOAP utilicé también la referencia de Kannan et al. (2026) y el recorte anotado compartido por Juliana, conservando su autoría.
- **Problema y solución:** El borrador local de la demo utilizaba SOAP 1.1, mientras los mensajes de las diapositivas correspondían a SOAP 1.2. Se ajustó la demo a SOAP 1.2 para mantener la coherencia.
- **Alcance:** La prueba funciona en localhost con un proveedor y códigos ficticios; no consulta registros académicos reales ni está integrada con el SSDC.
- **Evidencia Git:** Commits `79d47099`, `4d459a01`, `308f32cd`, `ac694d53`, `55548bf2`, `5cad3764` y `30ce3315`.
- **Uso de IA:** Utilicé ChatGPT (OpenAI) como apoyo para organizar y ajustar la estructura del código LaTeX de mis diapositivas y notas.