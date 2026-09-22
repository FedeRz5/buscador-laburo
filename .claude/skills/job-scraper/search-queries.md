# Búsquedas de empleo en Argentina

## Fuentes incluidas

- LinkedIn: puestos de distintos sectores, con ubicación Argentina o una ciudad argentina.
- Get on Board: tecnología y diseño; aplicar el filtro de país Argentina.
- FreeHire: tecnología, ingeniería y datos; aplicar `--country AR`.

## Comandos

```sh
python buscar.py "administrativo"
python buscar.py "atención al cliente" --ciudad "Córdoba"
python buscar.py "programador" --portal freehire --modalidad remoto
python buscar.py "diseñador" --portal getonbrd --modalidad remoto
```

Para ejecutar directamente los conectores, usar sus filtros explícitos de país. La interfaz `buscar.py` los agrega automáticamente.

## Consultas complementarias

```text
site:linkedin.com/jobs "[PUESTO]" "Argentina"
site:getonbrd.com "[PUESTO]" "Argentina"
"[EMPRESA]" "trabajá con nosotros" "Argentina"
```

Reemplazar los marcadores con los datos de la búsqueda. No ampliar a otros países automáticamente. Para trabajo remoto, confirmar que se acepten postulantes residentes en Argentina. Si el aviso no lo aclara, marcarlo como pendiente de verificar.

## Selección

Priorizar avisos de los últimos 14 días. Consultar ciudad, provincia, modalidad y distancia aceptable para puestos presenciales o híbridos. No asumir que Buenos Aires representa a todo el país. Si la fecha no está disponible, informar esa limitación.
