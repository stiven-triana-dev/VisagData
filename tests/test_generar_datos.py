from datetime import date, datetime

from datos.generar_datos import FIN, INICIO, cargar_catalogo, generar

DATOS = generar()


def test_siempre_genera_los_mismos_datos() -> None:
    assert generar() == DATOS


def test_los_clientes_no_tienen_datos_personales() -> None:
    assert set(DATOS["clientes"][0]) == {"cliente_id", "ciudad", "fecha_registro", "canal_registro"}


def test_usa_el_catalogo_real_con_sus_precios() -> None:
    precios = {p.id: p.precio for p in cargar_catalogo()}
    assert len(precios) == 108
    for item in DATOS["items_pedido"]:
        assert item["precio_unitario"] == precios[item["producto_id"]]


def test_las_tallas_vendidas_existen_en_el_catalogo() -> None:
    tallas = {p.id: set(p.tallas) for p in cargar_catalogo()}
    for item in DATOS["items_pedido"]:
        assert item["talla"] == "" or item["talla"] in tallas[item["producto_id"]]


def test_las_fechas_estan_dentro_del_periodo() -> None:
    for pedido in DATOS["pedidos"]:
        dia = datetime.fromisoformat(str(pedido["fecha_pedido"])).date()
        assert INICIO <= dia <= FIN


def test_nadie_compra_antes_de_registrarse() -> None:
    registro = {c["cliente_id"]: c["fecha_registro"] for c in DATOS["clientes"]}
    for pedido in DATOS["pedidos"]:
        assert str(registro[pedido["cliente_id"]]) <= str(pedido["fecha_pedido"])[:10]


def test_trae_datos_sucios_a_proposito_para_que_dbt_los_limpie() -> None:
    ciudades = {c["ciudad"] for c in DATOS["clientes"]}
    metodos = {p["metodo_pago"] for p in DATOS["pedidos"]}
    assert any(c != c.strip() or c.islower() for c in map(str, ciudades))
    assert len(metodos) > 3


def test_diciembre_vende_mas_que_enero() -> None:
    def pedidos_de(anio: int, mes: int) -> int:
        return sum(1 for p in DATOS["pedidos"] if str(p["fecha_pedido"]).startswith(f"{anio}-{mes:02d}"))

    assert pedidos_de(2025, 12) > pedidos_de(2026, 1)
    assert date(2025, 12, 1) == INICIO
