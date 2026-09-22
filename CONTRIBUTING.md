# Contribuir

Usá cambios pequeños y explicá qué problema resuelven. Conservá la licencia y las atribuciones de terceros.

## Verificación

Desde la raíz:

```sh
python -m unittest discover -s tests
python tools/security_guards.py
python tools/check_publication.py
python tools/lint_skills.py
```

El verificador de instrucciones requiere PyYAML. Para un conector modificado, instalá sus dependencias de desarrollo con `bun install` y ejecutá `bun run typecheck` y las pruebas locales pertinentes. Las pruebas que consultan portales reales se ejecutan manualmente.

Si cambiás plantillas LaTeX, compilalas e inspeccioná el resultado. No agregues los documentos compilados al repositorio.

## Datos y compatibilidad

Usá ejemplos ficticios y correos del dominio `example.com`. No incluyas currículums, teléfonos, perfiles, credenciales, capturas personales ni resultados de búsquedas privadas. Conservá los identificadores de comandos y campos de las API al traducir la documentación.

Describí en la propuesta los cambios, las comprobaciones realizadas y cualquier limitación conocida.
