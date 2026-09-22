---
name: linkedin-search
version: 1.1.0
description: >
  Buscar avisos públicos de LinkedIn en Argentina y consultar su detalle. Usar para buscar laburo, empleo, puestos remotos o vacantes por ciudad argentina, en cualquier sector.
context: fork
allowed-tools: Bash(bun run .agents/skills/linkedin-search/cli/src/cli.ts *)
---

# LinkedIn: empleo en Argentina

Usar el conector incluido; necesita Bun, sin sesión ni credenciales. Consulta el HTML público para visitantes y extrae avisos. Responder en español de Argentina y no enviar postulaciones.

## Búsqueda

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "administrativo" -l "Argentina" --jobage 14 --limit 10 --format json
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "atención al cliente" -l "Córdoba, Argentina" --format json
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "programador" -l "Argentina" --remote remote --format json
```

- País por defecto: Argentina. Si se indica ciudad, agregar `, Argentina`; no asumir CABA como ubicación de todas las personas.
- `--location` / `-l` es obligatorio. No usar `Remote` solo como ubicación: pierde el alcance argentino.
- `--query` / `-q`: puesto o palabras clave. Conservar términos habituales como QA, UX o DevOps.
- `--remote`: `remote`, `hybrid` u `onsite`; traducir desde remoto, híbrido o presencial.
- `--jobage`: `1`, `7`, `14` o `30` días. `--page` comienza en 1; cada llamada consulta una página con desplazamiento en bloques de diez.
- `--limit` recorta la respuesta; no recorre páginas adicionales. `--format`: `json`, `table` o `plain`.

## Detalle

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts detail <id|url> --format json
```

Usar un ID o enlace obtenido de resultados reales. Revisar descripción, ubicación, modalidad y condiciones de residencia antes de recomendar un puesto remoto. Si esas condiciones faltan, indicar que la elegibilidad para Argentina no está confirmada.

## Límites

Los errores salen por stderr con `error` y `code`, y código de salida 1. Ante bloqueos persistentes, informar el problema y detener las consultas; no evadir restricciones. Una lista vacía también puede deberse a cambios del HTML. El conector heredado está destinado a uso personal de bajo volumen; consultar las condiciones vigentes del sitio.

Guía de uso: `LINKEDIN.md` en la raíz. Contrato técnico: `cli/README.md` y `url-reference.md`.
