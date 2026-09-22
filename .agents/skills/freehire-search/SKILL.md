---
name: freehire-search
version: 1.1.0
description: >
  Buscar empleo de programación, datos, ingeniería y tecnología en Argentina mediante FreeHire. Usar para puestos técnicos, DevOps, QA o ML; no como fuente principal para empleos generales.
context: fork
allowed-tools: Bash(bun run .agents/skills/freehire-search/cli/src/cli.ts *)
---

# FreeHire: puestos técnicos en Argentina

Usar Bun y el conector local para consultar la API JSON. No requiere claves. Depende de un servicio externo: informar errores de disponibilidad sin prometer cobertura completa.

## Búsqueda

```sh
bun run .agents/skills/freehire-search/cli/src/cli.ts search -q "backend" --country AR --jobage 14 --format json
bun run .agents/skills/freehire-search/cli/src/cli.ts search -q "react" --country AR --remote remote --format json
bun run .agents/skills/freehire-search/cli/src/cli.ts search --category devops --country AR --format json
```

- Incluir `--country AR` en todas las búsquedas de este proyecto. No sustituirlo por una región más amplia.
- `--city` agrega una ciudad; el proveedor usa valores de un vocabulario controlado. No inventar valores de sus facetas. La referencia está en `url-reference.md`.
- `--query` / `-q`: palabras clave. `--seniority`, `--category` y `--skill` permiten refinar búsquedas técnicas.
- `--remote`: `remote`, `hybrid` u `onsite`. Comprobar residencia admitida en el aviso; el país de una faceta no garantiza elegibilidad contractual.
- `--jobage`: antigüedad en días; `--page` comienza en 1; `--limit` determina resultados por página. Formatos: `json`, `table`, `plain`.
- Las ofertas sin país normalizado pueden quedar fuera de `AR`. Informarlo, sin ampliar a otros países automáticamente.

## Detalle

```sh
bun run .agents/skills/freehire-search/cli/src/cli.ts detail <slug|url> --format json
```

Usar el `id`/slug o URL real de los resultados. Extraer únicamente datos presentes. Antes de recomendar, revisar fecha, ubicación y modalidad; conservar moneda y periodicidad salarial, sin inferir equivalencias.

La respuesta de búsqueda tiene `meta` y `results`. Los errores salen por stderr con `error` y `code`, código de salida 1. Si una fuente falla, informar la limitación y continuar con los otros portales disponibles.

`FREEHIRE_API_URL` permite apuntar a otra instancia compatible. Los detalles del protocolo se conservan en `cli/README.md` y `url-reference.md`.
