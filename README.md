# Servicios web: SOAP y REST

GA-SUM-01 / EXP-1 · Aplicaciones Distribuidas · Grupo CCEG.

La exposición analiza cómo aplicar servicios web a nuestros proyectos de fin de curso. Las prácticas muestran una consulta REST con control de acceso y dos intercambios SOAP con datos de prueba. Los diagramas distinguen el funcionamiento de las demos de la arquitectura que se propone para cada sistema.

## Integrantes

| Integrante | Tema |
| --- | --- |
| Kevin Leonel García Bazurto | REST para consultar turnos del RTV. |
| Khriz Alexander Coronel Gómez | REST para crear un registro. |
| Joseph Alexander Calderón Saltos | SOAP para verificar un título en un proveedor de prueba. |
| Juliana Romina Emanuel Pino | SOAP para validar una solicitud de reserva de laboratorio. |

## Documentos

- [Presentación en PDF](aportes/exposicion-soap-rest.pdf).
- [Archivo principal de Beamer](aportes/diapositiva-Garc%C3%ADa%20Kevin.tex).
- [Notas integradas en PDF](notas/notas.pdf) y [archivo principal LaTeX](notas/notas.tex).
- [Notas de cada integrante](notas/secciones/).
- [Diagramas editables e imágenes](diagramas/).
- [Bosquejos y evidencias de lectura](evidencias/).
- [Referencias BibLaTeX](referencias/).
- [Bitácora](BITACORA.md).

## Compilación

Se requiere una distribución LaTeX, como MiKTeX o TeX Live, con pdfLaTeX y Biber. La presentación utiliza Beamer, TikZ, babel español, Latin Modern, csquotes y biblatex. Las notas usan la clase article, geometry y los mismos paquetes de idioma y referencias.

Desde la raíz del repositorio, para generar las notas:

```powershell
cd notas
pdflatex notas.tex
biber notas
pdflatex notas.tex
pdflatex notas.tex
```

Para generar la presentación, desde la raíz:

```powershell
cd aportes
pdflatex "diapositiva-García Kevin.tex"
biber "diapositiva-García Kevin"
pdflatex "diapositiva-García Kevin.tex"
pdflatex "diapositiva-García Kevin.tex"
Copy-Item "diapositiva-García Kevin.pdf" "exposicion-soap-rest.pdf" -Force
```

Las imágenes y los archivos `.bib` se cargan con rutas relativas. Se debe conservar la estructura de carpetas al descargar o clonar el repositorio. El contenido de las notas integradas se reúne en `notas/contenido-integrado.tex`; las secciones individuales se conservan como material de cada responsable. El principal incorpora `notas/secciones/khriz.tex` cuando ese archivo existe.

## Prácticas

| Caso | Ejecución y resultados |
| --- | --- |
| [Kevin: consulta REST del RTV](demos/kevin/README.md) | Requiere Java 21, el backend del RTV y PostgreSQL. La [guía de prueba](demos/kevin/GUIA-DE-PRUEBA.md) explica cómo adaptar la cuenta, la vinculación y los identificadores. El turno propio devuelve 200 y el ajeno 404. |
| [Joseph: verificación SOAP](demos/joseph/README.md) | Desde `demos/joseph/`, ejecutar `python probar.py`. Requiere Python 3 y su biblioteca estándar. Comprueba WSDL, respuesta válida, respuesta no válida, SOAP Fault y tiempo de espera. |
| [Juliana: validación SOAP](demos/juliana/README.md) | Desde `demos/juliana/`, ejecutar `node practica-soap.mjs`. Requiere Node.js 18 o posterior. Comprueba el acuse de una solicitud completa y el SOAP Fault por hora de fin ausente. |

Las cuentas, los turnos y los mensajes utilizados son de prueba. El prototipo SOAP de Joseph no consulta un registro académico real. El acuse de Juliana comprueba los datos del ejemplo, no la disponibilidad real de un laboratorio. En el RTV, la cola de eventos y la base de lectura independiente forman parte de la evolución propuesta.

## Fuentes

Las notas citan los artículos y la documentación utilizados. Las dos referencias complementarias se exportaron desde Zotero en formato BibLaTeX y se contrastaron con el DOI y la publicación original:

- Camilleri, Vella y Nezval (2024): [consistencia causal y middleware distribuido](https://doi.org/10.3390/electronics13173367).
- Mabotha, Mabunda y Ali (2025): [APIs REST y despliegue con contenedores](https://doi.org/10.3390/s25102993).

Las capturas anotadas conservan la página del artículo. Los resultados de esas investigaciones no se presentan como mediciones de nuestras prácticas.

## Uso de inteligencia artificial

Se utilizó ChatGPT Sol 6.1 mediante Codex para ayudar a la integración de las notas de manera más sencilla, preparar este README de forma más clara. Las declaraciones de cada práctica se encuentran en su documentación y en la bitácora.
