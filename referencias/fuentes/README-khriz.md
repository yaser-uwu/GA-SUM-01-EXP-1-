# Fuentes del aporte de Khriz

## Comunicación síncrona y asíncrona

- Autores: Justas Kazanavičius y Dalius Mažeika.
- Título del PDF y de Crossref: *Evaluation of Microservice Communication While Decomposing Monoliths*. La página editorial antepone «The» al título; DOI, autores, revista, volumen y páginas corresponden a la misma obra.
- Revista: *Computing and Informatics*, 42(1), pp. 1–36, 2023.
- DOI: [10.31577/cai_2023_1_1](https://doi.org/10.31577/cai_2023_1_1).
- [Ficha editorial](https://www.cai.sk/ojs/index.php/cai/article/view/2023_1_1) y [PDF editorial](https://www.cai.sk/ojs/index.php/cai/article/download/2023_1_1/1208/17574).
- Archivo: `kazanavicius-mazeika-2023.pdf`, 36 páginas. La captura anotada de `evidencias/khriz-articulo-comunicacion-anotado.png` conserva la p. 3, apartado 2.1, sobre la espera de respuesta en comunicación síncrona.
- Aplicación: justificar la dependencia temporal del cliente respecto de la API y contrastarla con mensajería. No se trasladan al SGRA las cifras del experimento.
- Indexación: la [página oficial de la revista](https://www.cai.sk/ojs/index.php/cai/index) declara Scopus, INSPEC y otros índices. Se contrastó esa declaración editorial; no se realizó una consulta independiente en Scopus. El DOI no se usa como prueba de indexación.

## CAP y PACELC

Se contrastaron en Crossref los DOI, autores, títulos, revista, volumen, número y páginas de Gilbert y Lynch (2002), DOI `10.1145/564585.564601`, y Abadi (2012), DOI `10.1109/MC.2012.33`. Sus referencias están en el BibLaTeX de Khriz. Son antecedentes fundacionales y no cuentan para el mínimo de fuentes recientes de la actividad.

## Procedencia funcional

RF01 del [PFC-SGRA](https://github.com/Yukisan-uwo/PFC-SGRA/blob/main/docs/secciones/06-requisitos.tex) describe la solicitud de refuerzo, la disponibilidad preferida y el estado Pendiente. El [controlador del backend anterior](https://github.com/BelindaTZ/SEG-INF-back-SGRA-Docker/blob/main/src/main/java/com/CLMTZ/Backend/controller/reinforcement/student/StudentRequestController.java) permite contrastar la ruta y las validaciones iniciales. La demo autónoma y su JSON simplificado se distinguen del sistema existente en la guía de prueba.

La consulta y la anotación fueron preparadas con asistencia de OpenAI Codex. Khriz debe leer los pasajes, revisar las fuentes y explicar su aplicación antes de la exposición.
