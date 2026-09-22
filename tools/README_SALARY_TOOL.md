# Referencias salariales de Argentina

`salary_lookup.py` consulta un archivo privado `salary_data.json` que aportás vos. El repositorio no incluye sueldos reales ni calcula un salario de mercado por sí solo.

```sh
python salary_lookup.py "Empresa de ejemplo" --city "Córdoba" --json
```

El buscador tolera diferencias de mayúsculas y tildes y reconoce razones sociales SA, SRL y SAS, con o sin puntos. El filtro de ciudad también admite texto sin tildes.

## Formato

El JSON contiene `metadata` y una lista `companies`. Cada empresa tiene `company`, `city` y `categories`; cada categoría puede tener `count` e `index`.

```json
{
  "metadata": {
    "source": "Ejemplo ficticio: reemplazar con la fuente real",
    "index_label": "Índice salarial",
    "index_baseline": 100,
    "baseline_description": "100 = referencia de la muestra"
  },
  "companies": [
    {
      "company": "Empresa de ejemplo SRL",
      "city": "Córdoba",
      "categories": {"administración": {"count": 10, "index": 105}}
    }
  ]
}
```

Los números del ejemplo son ficticios; son índices, no importes en pesos. Si cargás importes, indicá moneda, fecha de referencia, período y condición bruto/neto en los metadatos. Usá `index_baseline: 0` para evitar porcentajes comparativos cuando no corresponden. No mezcles ARS y USD ni períodos distintos bajo una misma referencia: la herramienta no convierte monedas ni ajusta por inflación.

## Importar una planilla

Requiere `openpyxl`. El conversor reconoce `Empresa` o `Razón social`, `Ciudad` o `Localidad`, y columnas numéricas de `cantidad`, `índice`, `salario` o `sueldo`. También admite encabezados equivalentes en inglés.

```sh
python tools/convert_salary_excel.py datos.xlsx --source "Mi fuente y fecha de referencia"
```

Para agrupar una categoría usá, por ejemplo, `Administración cantidad` y `Administración índice`. Revisá el JSON generado antes de usarlo. Tanto la planilla como `salary_data.json` son privados y quedan excluidos de Git.
