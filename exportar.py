"""Exporta las tablas finales de DuckDB a CSV para Power BI (carpeta powerbi/datos).

Uso (después de `dbt build`):  python exportar.py
Los CSV van en UTF-8 con BOM para que Power BI y Excel reconozcan las tildes.
"""

import csv
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parent
BASE = RAIZ / "visag_ventas.duckdb"
SALIDA = RAIZ / "powerbi" / "datos"
TABLAS = [
    # modelo estrella (para relacionar en Power BI)
    "fct_ventas",
    "dim_productos",
    "dim_clientes",
    # reportes ya calculados
    "ventas_mensuales",
    "ventas_categoria_mes",
    "productos_top",
    "ventas_por_ciudad",
    "ventas_por_talla",
    "pedidos_por_estado",
]


def exportar(base: Path = BASE, salida: Path = SALIDA) -> list[Path]:
    salida.mkdir(parents=True, exist_ok=True)
    archivos = []
    with duckdb.connect(str(base), read_only=True) as conexion:
        for tabla in TABLAS:
            destino = salida / f"{tabla}.csv"
            datos = conexion.sql(f"select * from {tabla} order by all")  # noqa: S608 (nombres fijos de la lista)
            filas = [datos.columns, *datos.fetchall()]
            with destino.open("w", encoding="utf-8-sig", newline="") as archivo:
                csv.writer(archivo).writerows(
                    ["" if v is None else (str(v).lower() if isinstance(v, bool) else v) for v in fila]
                    for fila in filas
                )
            archivos.append(destino)
    return archivos


if __name__ == "__main__":
    for archivo in exportar():
        print(archivo.relative_to(RAIZ))
