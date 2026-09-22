# Configuración

## Herramientas

- Bun: ejecuta los conectores TypeScript de `.agents/skills/`.
- Python 3.10 o posterior: ejecuta verificaciones y las utilidades salariales.
- LuaLaTeX y XeLaTeX: compilan CV y cartas, respectivamente.
- Poppler (`pdftotext`): comprueba la extracción de texto para sistemas de selección.

Los conectores incluyen instrucciones específicas en su carpeta `cli/`. Para desarrollar uno, ejecutá `bun install` dentro de esa carpeta y luego `bun run typecheck`.

## Buscar ofertas

```sh
python buscar.py "administrativo"
python buscar.py "programador" --portal freehire --modalidad remoto
python buscar.py "diseñador" --portal getonbrd
python buscar.py --help
```

El país configurado es Argentina; no hay una persona ni una ciudad preconfiguradas. Consultá [ARGENTINA.md](ARGENTINA.md) para ver filtros y límites por portal.

## Preparar postulaciones

En una copia privada, colocá los documentos en las subcarpetas de `documents/` y usá `/setup` para cargar tu perfil. También podés aportar un CV o completar los datos mediante preguntas. Confirmá la información extraída antes de usarla.

Después usá `/apply` con el texto o enlace de una oferta. El CV y la carta deben respetar el idioma del aviso; ante ambigüedad, se usa español. No se deben inventar experiencia ni competencias.

## Compilar los ejemplos

```sh
cd cv
lualatex -interaction=nonstopmode main_example.tex
cd ../cover_letters
xelatex -interaction=nonstopmode cover_example.tex
```

Son ejemplos con campos vacíos, no documentos listos para postular. Los PDF generados se excluyen de Git.

## Publicar cambios

Mantené los perfiles públicos vacíos y ejecutá `python tools/check_publication.py` desde la raíz. Revisá `git diff`, `git diff --cached` y el historial. `.gitignore` no elimina datos ya guardados en commits ni protege archivos que ya están versionados. No publiques una copia personalizada sin limpiarla primero.
