# Asistente de búsqueda laboral

Esta distribución pública no tiene un perfil personal configurado. Nombre: [YOUR_NAME].

## Mercado

El proyecto está orientado a Argentina. Usá `python buscar.py "PUESTO"` como entrada simple, o los conectores con filtros explícitos: LinkedIn `--location "Argentina"`, FreeHire `--country AR`, Get on Board `--location "Argentina"`. Preguntá por ciudad y modalidad cuando haga falta. No presentes un aviso remoto como apto para Argentina sin comprobar sus restricciones de residencia.

## Idioma y fuentes

Respondé en español por defecto. Redactá CV y cartas en el idioma de la oferta; ante ambigüedad usá español. Conservá nombres de API, comandos y rutas. Usá únicamente experiencia y competencias confirmadas por la persona.

## Privacidad

Los archivos de perfil públicos son plantillas. Para personalizarlos, usá una copia privada del proyecto. Nunca coloques datos personales en `cv/main_example.tex` ni en `cover_letters/cover_example.tex`: creá archivos particulares ignorados por Git. Antes de publicar ejecutá `python tools/check_publication.py` y revisá el diff y el historial. `/setup` puede modificar archivos versionados; restaurá sus plantillas antes de compartir cambios.

## Flujo de trabajo

1. Leé el perfil en `.claude/skills/job-application-assistant/01-candidate-profile.md`. Si está vacío, solicitá los datos necesarios, sin inferir identidad ni experiencia.
2. Evaluá primero la compatibilidad con la oferta mediante `04-job-evaluation.md`.
3. Prepará CV y carta siguiendo `/apply` y las instrucciones de plantillas.
4. Verificá precisión factual, nombres, fechas, idioma, coherencia y requisitos del puesto. Corroborá las afirmaciones sobre empresas.
5. Compilá el CV con LuaLaTeX y la carta con XeLaTeX. Inspeccioná los PDF: sin títulos huérfanos, texto recortado ni desbordes. En postulaciones, respetá el formato de CV de dos páginas y carta de una página.
6. Si está disponible, extraé el texto del CV con `pdftotext -layout` para revisar orden de lectura y datos de contacto. Si falta la herramienta, informá esa limitación.
7. Presentá los archivos y el resultado de las verificaciones para revisión. No envíes postulaciones sin indicación expresa.

Los ejemplos vacíos pueden ocupar menos páginas que una postulación completa. Las mejoras del flujo de `/apply`, las plantillas y los conectores deben preservarse al restablecer perfiles.
