# EXP-1: servicios web SOAP y REST — Grupo CCEG

Material de exposición sobre aplicaciones de SOAP y REST a los PFC del equipo. La adaptación al enfoque de los cuatro PFC debe confirmarse con el docente según la ficha de reparto; este repositorio no acredita esa aprobación.

| Integrante | Aporte |
| --- | --- |
| Kevin García | [Consulta REST de turnos RTV](demos/kevin/README.md). |
| Khriz Coronel | [Registro REST de solicitudes SGRA](demos/khriz/README.md). |
| Joseph Calderón | Propuesta SOAP para verificar títulos académicos. |
| Juliana Emanuel | [Validación SOAP de reservas CLAB](demos/juliana/README.md). |

## Demo de Khriz

Requiere Node.js 18 o posterior. Desde la raíz del repositorio:

```powershell
node demos/khriz/probar-rest.mjs
node demos/khriz/servidor-rest.mjs
```

El primer comando comprueba 12 escenarios y termina. El segundo mantiene el servicio manual en `127.0.0.1:8083`; se detiene con Ctrl+C. La guía de la demo incluye los dos POST, los resultados conservados y las limitaciones del prototipo.

## Compilar diapositivas y notas

Se necesita una distribución LaTeX con **pdfLaTeX y Biber**, Beamer, TikZ, babel español, Latin Modern, csquotes, biblatex con estilo IEEE, geometry, tabularx y booktabs. Las diapositivas usan `aportes/diapositiva-García Kevin.tex` como archivo principal.

Desde `aportes/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error "diapositiva-García Kevin.tex"
biber "diapositiva-García Kevin"
pdflatex -interaction=nonstopmode -halt-on-error "diapositiva-García Kevin.tex"
pdflatex -interaction=nonstopmode -halt-on-error "diapositiva-García Kevin.tex"
```

El PDF para compartir se conserva como `aportes/exposicion-soap-rest.pdf`, copia del resultado de la compilación. Véase también [la guía del grupo](aportes/readme.md).

Las notas individuales de Khriz se pueden compilar desde `notas/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error khriz.tex
biber khriz
pdflatex -interaction=nonstopmode -halt-on-error khriz.tex
pdflatex -interaction=nonstopmode -halt-on-error khriz.tex
```

Se genera `notas/khriz.pdf`. Su sección editable está en `notas/secciones/khriz.tex`. El resumen de su turno forma parte de [las notas grupales](notas/notas.tex). Para generar `notas/notas.pdf`, aplicar la misma secuencia desde `notas/` con `notas.tex` y `biber notas`.

## Ensayo y evidencias pendientes

[Video grupal en YouTube](https://www.youtube.com/watch?v=CkRA7jrbEpk). El equipo debe verificar que la grabación corresponda a la versión que presenta y que cumpla los requisitos de acceso, duración y participación.

Queda por verificar la fotografía del bosquejo grupal con nombres y fecha y completar la trazabilidad de los aportes de cada persona. La captura anotada de Khriz fue preparada con asistencia de Codex. El equipo debe verificar el cumplimiento de las fuentes y las formativas.

El código `GA-SUM-01` se conserva en la portada existente; el enunciado general aportado indica `GA-SUM-02`. El equipo debe confirmar el código aplicable antes de la entrega. El README no acredita entrega en el SGA ni aprobación de la adaptación temática.
