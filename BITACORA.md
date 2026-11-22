# Bitácora del equipo CCEG — EXP-1

## 2026-11-18 — Kevin Leonel García Bazurto

- **Presentes:** Kevin Leonel García Bazurto.
- **Realizado:** Se definió la consulta REST de turnos del sistema de Revisión Técnica Vehicular y se publicó el bosquejo a mano de la propuesta.
- **Problemas encontrados:** Había que diferenciar la consulta del solicitante de las funciones del personal.
- **Solución:** Se planteó una aplicación externa para consultar el turno, sin permitir el acceso a las funciones internas.
- **Uso de inteligencia artificial:** Se utilizó ChatGPT Sol 6.1 mediante Codex para preparar el diseño y apoyar la explicación del flujo.

## 2026-11-20 — Kevin Leonel García Bazurto

- **Presentes:** Kevin Leonel García Bazurto.
- **Realizado:** Se publicaron el diagrama editable y su imagen, las notas y las diapositivas. Se preparó la demo REST con el backend y PostgreSQL del RTV. El turno propio devolvió 200 y el ajeno 404. Se conservaron las peticiones, respuestas y capturas. Se incorporó un artículo sobre evolución de API, su referencia exportada de Zotero y una captura anotada.
- **Problemas encontrados:** El solicitante necesitaba consultar solo los turnos del propietario vinculado con su cuenta. También había que separar lo implementado de la arquitectura futura.
- **Solución:** Se incorporó la comprobación del vínculo entre usuario, propietario y turno. La cola, el consumidor y la base de lectura se identificaron como parte de la propuesta.
- **Uso de inteligencia artificial:** Se utilizó ChatGPT Sol 6.1 mediante Codex para ayudarme y guiarme con la preparación de código, documentación y material de exposición, y para que me ayude a comprobar las respuestas de la demo y la compilación.

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
