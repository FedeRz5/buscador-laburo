# Buscador de empleo con IA

Herramientas de búsqueda de ofertas laborales y asistencia para preparar postulaciones. Esta adaptación incorpora Get on Board para Latinoamérica y prioriza el español en los documentos y la interacción.

Permite buscar en LinkedIn, FreeHire, Get on Board y varios portales de Dinamarca; evaluar ofertas, adaptar un CV, redactar cartas y preparar entrevistas. Los conectores se ejecutan desde la terminal con Bun. Los flujos de asistencia están definidos en `.claude/`.

## Inicio rápido

Requisitos: Bun para los conectores; Python 3 para las herramientas salariales y verificaciones. Para generar documentos se necesitan LuaLaTeX y XeLaTeX.

Desde la raíz del repositorio:

```sh
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --category design-ux --remote --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts --help
```

Consultá [SETUP.md](SETUP.md) para configurar el entorno. Los nombres de comandos, opciones y campos JSON se mantienen para conservar compatibilidad.

## Buscar en LinkedIn

Consultá la [guía de LinkedIn en español](LINKEDIN.md): explica cómo funciona el scraper, qué necesitás y cómo buscar por puesto, ubicación y modalidad, con ejemplos para Argentina.

## Flujos disponibles

| Comando | Función |
|---------|---------|
| `/setup` | Configurar un perfil con información proporcionada por la persona |
| `/apply` | Evaluar una oferta y preparar CV y carta |
| `/rank` | Comparar ofertas |
| `/interview` | Preparar entrevistas |
| `/outcome` | Registrar resultados de postulaciones |
| `/expand` | Ampliar la búsqueda |
| `/add-portal` | Incorporar un portal |
| `/add-template` | Registrar una plantilla |
| `/reset` | Reiniciar la configuración personal |

## Estructura

- `.agents/skills/`: conectores y documentación técnica de cada portal.
- `.claude/`: instrucciones de asistencia, comandos y plantillas de perfil.
- `cv/` y `cover_letters/`: ejemplos LaTeX sin datos personales.
- `documents/`: documentos privados de entrada, excluidos de Git.
- `job_scraper/` y `upskill/`: resultados privados generados.
- `tools/` y `tests/`: utilidades y pruebas.

## Privacidad antes de publicar

Esta distribución contiene plantillas vacías. No reemplaces los ejemplos públicos con un CV real. `/setup` puede modificar archivos que Git ya sigue: `.gitignore` no protege esos cambios. Trabajá con datos personales en una copia privada y revisá el diff antes de publicar.

```sh
python tools/check_publication.py
python tools/security_guards.py
python -m unittest discover -s tests
```

La revisión automática es una ayuda, no una garantía: revisá también los cambios y el historial. No subas la carpeta `.git` como archivo adjunto ni compartas una copia completa de tu espacio privado.

## Alcance

Las ofertas cambian y cada portal tiene sus propias condiciones y límites. Las pruebas de red se ejecutan de forma manual. La comparación salarial requiere un archivo local `salary_data.json`; no incluye datos salariales personales en esta distribución.

## Origen y licencia

Adaptación de [ai-job-search de Mads Lorentzen](https://github.com/MadsLorentzen/ai-job-search), con licencia MIT. Se conserva el aviso original en [LICENSE](LICENSE). Las modificaciones de esta adaptación no implican autoría exclusiva sobre el proyecto original.
