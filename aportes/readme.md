# Presentación SOAP y REST

El archivo principal es `diapositiva-García Kevin.tex`. Reúne las secciones de todo el grupo.

| Integrante | Archivo que edita | Tema |
| --- | --- | --- |
| Kevin | `kevin.tex` | REST para consultar turnos del RTV |
| Khriz | `khriz.tex` | REST para registrar |
| Joseph | `joseph.tex` | SOAP para verificar |
| Juliana | `juliana.tex` | SOAP para validar |

Cada integrante crea su propio archivo y agrega sus diapositivas con `\begin{frame}{Título}` y `\end{frame}`, sin repetir `\documentclass` ni `\begin{document}`. Todos usan el diseño de `estilo.tex`. El documento principal incorpora los archivos de los compañeros cuando ellos los crean.

Las referencias se guardan en `../referencias/referencias-NOMBRE.bib`, usando el nombre en minúsculas. El documento principal carga los archivos de referencias de cada integrante cuando existen. Las citas se añaden con `\cite{clave}` y la bibliografía se genera al final.

## Compilación

Desde esta carpeta:

```powershell
pdflatex "diapositiva-García Kevin.tex"
biber "diapositiva-García Kevin"
pdflatex "diapositiva-García Kevin.tex"
pdflatex "diapositiva-García Kevin.tex"
```

Se requiere una distribución LaTeX con Beamer, TikZ, babel español, Latin Modern, csquotes, biblatex y Biber. El PDF para compartir es `exposicion-soap-rest.pdf`; se obtiene renombrando una copia del PDF generado.
