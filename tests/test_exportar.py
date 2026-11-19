from pathlib import Path

import duckdb

import exportar


def test_exporta_cada_tabla_con_tildes_y_nulos_vacios(tmp_path: Path, monkeypatch) -> None:
    base = tmp_path / "prueba.duckdb"
    with duckdb.connect(str(base)) as conexion:
        for tabla in exportar.TABLAS:
            conexion.execute(f"create table {tabla} as select 'Girón' as ciudad, null as valor, true as es_venta")
    archivos = exportar.exportar(base, tmp_path / "salida")

    assert len(archivos) == len(exportar.TABLAS)
    contenido = archivos[0].read_bytes()
    assert contenido.startswith(b"\xef\xbb\xbf")
    assert contenido.decode("utf-8-sig").splitlines() == ["ciudad,valor,es_venta", "Girón,,true"]
