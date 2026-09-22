# Cómo buscar trabajo en LinkedIn

Este proyecto incluye un scraper de **ofertas laborales públicas de LinkedIn**. Le indicás un puesto y una ubicación, y te devuelve los avisos que puede leer, con sus datos y enlaces.

No necesitás cargar un currículum ni configurar un perfil para hacer una búsqueda. El conector no inicia sesión en tu cuenta y no envía postulaciones: sirve para encontrar y consultar avisos.

## Cómo funciona por dentro

1. Recibe las palabras clave, la ubicación y los filtros que escribís en la terminal.
2. Arma una consulta al endpoint público `jobs-guest/jobs/api/seeMoreJobPostings/search` de LinkedIn.
3. Descarga el HTML de la respuesta y extrae las ofertas con expresiones regulares.
4. Muestra los resultados como tabla, texto o JSON.
5. Si pedís el detalle de una oferta, consulta `jobs-guest/jobs/api/jobPosting/<id>` y extrae la descripción y los campos disponibles.

Es scraping de las páginas públicas para visitantes. No usa una API oficial de desarrolladores con credenciales ni lee perfiles privados. La búsqueda del conector se hace con código TypeScript; no necesita un modelo de IA para ejecutarse. Los flujos de IA del proyecto sirven después para evaluar ofertas o preparar documentos.

## Qué necesitás

Tenés que tener Bun instalado y conexión a internet. Abrí una terminal en la carpeta principal del repositorio y comprobá que Bun esté disponible:

```sh
bun --version
```

Este conector no tiene dependencias de ejecución externas. Para usarlo no hace falta correr `bun install`; ese paso se usa para las herramientas de desarrollo.

## Entrada simple para Argentina

Desde la raíz podés usar `python buscar.py "administrativo" --ciudad "Córdoba"`. El comando agrega Argentina como país y usa LinkedIn por defecto. Consultá [ARGENTINA.md](ARGENTINA.md) para todos los filtros. Los comandos directos de esta guía también siguen disponibles.

## Hacer tu primera búsqueda

Por ejemplo, para buscar puestos administrativos en Argentina publicados en los últimos siete días:

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "administrativo" -l "Argentina" --jobage 7 --format table
```

Cambiá `administrativo` por el puesto que te interese y `Argentina` por la ubicación que quieras. Poné los textos entre comillas si contienen espacios.

### Buscar en una ciudad

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "atención al cliente" -l "Buenos Aires, Argentina" --format plain
```

### Buscar puestos remotos

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "desarrollador frontend" -l "Argentina" --remote remote --jobage 7 --format plain
```

El filtro remoto no garantiza que puedas trabajar desde cualquier país. Revisá las condiciones del aviso, incluidos residencia, horarios y modalidad de contratación.

### Consultar otra página

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "administrativo" -l "Argentina" --page 2 --limit 5 --format plain
```

Cada ejecución consulta una página; no recorre todos los resultados automáticamente. El código calcula el desplazamiento en bloques de diez. `--limit` recorta los resultados recibidos: no descarga páginas adicionales para alcanzar esa cantidad ni reduce por sí solo la cantidad de solicitudes.

## Ver la descripción de una oferta

Copiá el ID o el enlace de una oferta de los resultados y usá `detail`. Reemplazá el texto entre comillas por el ID real:

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts detail "ID_DE_LA_OFERTA" --format plain
```

También podés pasar una URL de la oferta en lugar del ID. El detalle puede incluir descripción, nivel de experiencia, tipo de empleo, área, industria y enlace para postularte, según lo que devuelva LinkedIn.

## Opciones de búsqueda

| Opción | Para qué sirve |
|--------|----------------|
| `--query` o `-q` | Puesto, competencia o palabras clave |
| `--location` o `-l` | Ubicación; es obligatoria |
| `--jobage` | Antigüedad: `1`, `7`, `14` o `30` días; si lo omitís, no se agrega este filtro |
| `--remote` | Modalidad: `remote`, `hybrid` u `onsite` |
| `--page` | Página que querés consultar; empieza en `1` |
| `--limit` o `-n` | Máximo de resultados que se muestran de esa respuesta |
| `--format` | `json`, `table` o `plain`; por defecto usa `json` |

Para ver la ayuda del programa:

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search --help
```

Los nombres de las opciones y algunos mensajes de la terminal siguen en inglés. Escribilos tal como aparecen en los ejemplos.

## Qué devuelve

La búsqueda devuelve ID, título, empresa, ubicación, fecha y enlace, cuando están disponibles. La tabla abrevia los textos largos; usá `plain` para ver los enlaces o `json` para procesar los resultados con otro programa.

En JSON, la búsqueda devuelve `meta` y `results`. `meta.count` indica cuántos resultados se emitieron en esa ejecución, no el total de vacantes en LinkedIn. Algunos campos pueden venir vacíos.

Los resultados se imprimen en la terminal. Si querés guardarlos, podés redirigir la salida a la carpeta privada `job_scraper/`, que está excluida de Git:

```sh
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "administrativo" -l "Argentina" --format json > job_scraper/linkedin-resultados.json
```

## Si algo falla

- **No se reconoce `bun`:** comprobá la instalación y volvé a abrir la terminal.
- **`NO_LOCATION`:** agregá `-l "Argentina"` o la ubicación que corresponda.
- **`BAD_ID`:** usá el ID o enlace real de una oferta; el marcador del ejemplo no es un aviso válido.
- **`SEARCH_FAILED` o `DETAIL_FAILED`:** revisá el mensaje. Puede deberse a un error de red o a una respuesta de rechazo del sitio.
- **Respuesta HTTP 429 o 5xx:** el código hace hasta seis reintentos con esperas crecientes. Si sigue fallando, dejá de consultar y probá más tarde.
- **Sin resultados:** probá otras palabras clave o menos filtros. También puede haber cambiado el HTML o haberse recibido una página de bloqueo que el parser no reconoce; una lista vacía no prueba que no existan vacantes.

Los errores se escriben por separado en la salida de errores (`stderr`) como JSON y el programa termina con código `1`.

## Alcance y uso

El conector está pensado para consultas personales de bajo volumen. La documentación heredada advierte sobre restricciones de LinkedIn al acceso automatizado; revisá las condiciones vigentes antes de usarlo. No incluye mecanismos para sortear bloqueos ni acceder a contenido privado.

Esta guía describe el código incluido en el repositorio. No certifica que LinkedIn responda correctamente en este momento: el sitio puede cambiar sus páginas o restringir las consultas. Antes de postularte, abrí el enlace y verificá que el aviso siga vigente.
