# Buscar laburo en Argentina

## Ejemplos por ciudad y sector

```sh
python buscar.py "administrativo" --ciudad "Buenos Aires" --modalidad hibrido
python buscar.py "atención al cliente" --ciudad "Córdoba"
python buscar.py "vendedor" --ciudad "Rosario"
python buscar.py "analista de datos" --ciudad "Mendoza"
python buscar.py "programador" --modalidad remoto
```

Las ciudades son ejemplos, no la ubicación de una persona preconfigurada. Si omitís `--ciudad`, se busca en Argentina. Escribí una localidad argentina y revisá la ubicación devuelta por el portal.

## Opciones del comando

| Opción | Valores |
|--------|---------|
| `--portal` | `linkedin` (predeterminado), `getonbrd`, `freehire` |
| `--ciudad` | Ciudad argentina; LinkedIn y FreeHire |
| `--modalidad` | `remoto`, `hibrido`, `presencial`; si se omite, todas |
| `--dias` | `1`, `7`, `14` (predeterminado), `30` |
| `--limite` | Número positivo; predeterminado: 10 |
| `--pagina` | Número positivo; predeterminado: 1 |
| `--formato` | `texto` (predeterminado), `tabla`, `json` |

Get on Board admite el filtro remoto, pero no filtros de ciudad, híbrido o presencial. Si se piden, el comando explica la limitación en lugar de ignorarlos.

## Cómo se aplica el país

`buscar.py` ejecuta uno de los conectores incluidos y agrega:

- LinkedIn: `--location "Argentina"` o `--location "CIUDAD, Argentina"`.
- FreeHire: `--country AR`, más `--city` si corresponde.
- Get on Board: `--location "Argentina"`, aplicado sobre los países informados en los avisos de la página recibida.

No elimina filtros para llenar resultados ni amplía automáticamente a otros países. Esto puede dejar fuera avisos remotos que no declaran Argentina aunque podrían aceptar postulantes del país. Ningún filtro reemplaza la lectura del aviso.

Se consulta una página por ejecución. `--limite` es un máximo, no una cantidad garantizada ni una búsqueda de todas las páginas. El comando tiene un tiempo máximo de dos minutos e informa fallas de conexión o del portal.

## Guardar resultados

```sh
python buscar.py "administrativo" --formato json > job_scraper/resultados-argentina.json
```

La carpeta `job_scraper/` es privada y se excluye de Git. No subas resultados con datos de contacto personales.

## Qué revisar antes de postularte

Verificá ciudad, modalidad, fecha, requisitos, residencia permitida y enlace de postulación. Si se menciona remuneración, distinguí ARS o USD, bruto o neto, y período. No se calculan conversiones de moneda ni sueldos de mercado automáticamente. Los CV se redactan en español salvo que la oferta pida otro idioma.

Los conectores usan fuentes externas: pueden cambiar o dejar de responder. Las pruebas del proyecto verifican el código y los filtros con datos de prueba; no garantizan disponibilidad ni cobertura completa de ofertas reales.
