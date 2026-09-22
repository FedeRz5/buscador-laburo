# Buscador de Laburo 🇦🇷

Búsqueda de empleo en Argentina desde la terminal, con filtros por puesto, ciudad y modalidad. Adaptación y desarrollo local por **Federico Reiz**.

Reúne conectores de LinkedIn, Get on Board y FreeHire. También incluye instrucciones de IA para evaluar ofertas, preparar un CV, redactar cartas y practicar entrevistas. Podés buscar avisos sin cargar datos personales ni usar un modelo de IA.

## Arrancá por acá

Necesitás **Python 3.10 o posterior**, **Bun** y conexión a internet. Desde la carpeta del proyecto:

```sh
python buscar.py "administrativo"
python buscar.py "atención al cliente" --ciudad "Córdoba" --modalidad presencial
python buscar.py "programador" --modalidad remoto --dias 7
```

Por defecto busca en LinkedIn, en Argentina, durante los últimos 14 días y muestra hasta 10 resultados de una página. No envía postulaciones ni inicia sesión en tu cuenta.

## Elegí dónde buscar

| Portal | Uso | Filtros locales |
|--------|-----|----------------|
| LinkedIn | Puestos de distintos sectores | País, ciudad y modalidad |
| Get on Board | Tecnología, diseño y UX | País; filtro remoto opcional |
| FreeHire | Programación, ingeniería y datos | País, ciudad y modalidad según los datos del proveedor |

```sh
python buscar.py "diseñador" --portal getonbrd
python buscar.py "backend" --portal freehire --modalidad remoto
python buscar.py "ventas" --ciudad "Rosario" --formato json
python buscar.py --help
```

Todos los comandos de `buscar.py` agregan el filtro de Argentina. Los conectores de bajo nivel conservan sus opciones técnicas, por lo que si los ejecutás directamente tenés que pasar el país explícitamente. El filtro remoto no garantiza que acepten residentes argentinos: revisá el aviso. En Get on Board, las ofertas sin país declarado pueden quedar fuera; su filtro tampoco permite buscar por ciudad.

## Guías

- [Configurar el proyecto](SETUP.md).
- [Cómo funciona el scraper de LinkedIn](LINKEDIN.md).
- [Filtros, ejemplos y alcance de Argentina](ARGENTINA.md).
- [Referencias salariales con datos propios](tools/README_SALARY_TOOL.md).

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

Buscador de Laburo es una adaptación de Federico Reiz para Argentina, basada en [ai-job-search de Mads Lorentzen](https://github.com/MadsLorentzen/ai-job-search). Se distribuye con licencia MIT; [LICENSE](LICENSE) conserva los avisos de autoría del código original y de las modificaciones.
