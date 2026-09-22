# Plantillas personalizadas

`/add-template` permite registrar plantillas LaTeX para CV y cartas. Cada plantilla se guarda en `cv/<nombre>/` o `cover_letters/<nombre>/`, con `template.tex`, un manifiesto `TEMPLATE.md` y los archivos de estilo o fuentes necesarios.

El manifiesto describe motor de compilación, tipografías, límite de páginas y reglas de diseño. Usá marcadores vacíos en lugar de nombres y datos reales.

- `/add-template --list`: mostrar plantillas.
- `/add-template --use <nombre>`: activar una plantilla.
- `/add-template --use default`: volver al formato incluido.

Antes de compartir una plantilla, revisá su contenido y los metadatos de sus recursos. Conservá las licencias de fuentes y estilos.
