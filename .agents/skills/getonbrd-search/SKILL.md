---
name: getonbrd-search
version: 1.1.0
description: >
  Buscar puestos de tecnología, diseño y UX en Get on Board para Argentina. Usar para empleos de diseño, programación, producto, datos o trabajo remoto con residencia en Argentina.
context: fork
allowed-tools: Bash(bun run .agents/skills/getonbrd-search/cli/src/cli.ts *)
---

# Get on Board: tecnología y diseño para Argentina

Ejecutar el conector con Bun. La búsqueda consulta JSON y el detalle lee el HTML del aviso. No requiere cargar un CV ni iniciar sesión.

## Búsqueda

```sh
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --category design-ux --location "Argentina" --jobage 14 --format json
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search -q "programador" --location "Argentina" --format json
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --category programming --location "Argentina" --remote --format json
```

- Incluir siempre `--location "Argentina"` para conservar el alcance local.
- Se necesita `--category` o `--query`. Categorías de ejemplo: `design-ux`, `programming`, `data-science-analytics`, `sysadmin-devops-qa`.
- Con categoría, `--query` filtra títulos dentro de la página recibida; sin categoría, consulta búsqueda de texto.
- Ubicación, fecha y modalidad se filtran localmente después de descargar una página. La ubicación compara el campo de países, no ciudades.
- `--remote` es un indicador sin valor. No admite filtros específicos para híbrido o presencial; usar LinkedIn para eso.
- `--page` comienza en 1. `--limit` recorta resultados e influye en el tamaño de página, con un máximo solicitado de 50. `--format`: `json`, `table` o `plain`.

## Remoto y datos incompletos

Un aviso etiquetado solo como remoto puede no declarar Argentina y quedar fuera del filtro. Informar esa limitación; no quitar el filtro silenciosamente ni afirmar que remoto significa desde cualquier país. Verificar la residencia admitida en la descripción antes de recomendarlo. Una página sin coincidencias no significa que el portal completo esté vacío.

## Detalle

```sh
bun run .agents/skills/getonbrd-search/cli/src/cli.ts detail <slug|url> --format json
```

Copiar el `id` o URL real de los resultados; no inventar slugs. Los campos ausentes se informan como desconocidos. No asumir moneda, sueldo neto ni modalidad contractual a partir del nombre del portal.

Errores: stderr con `error` y `code`, salida 1. Mantener bajo volumen y detener consultas si hay bloqueos persistentes. Referencia técnica en `url-reference.md` y `cli/README.md`.
