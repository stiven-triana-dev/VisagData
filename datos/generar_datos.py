from __future__ import annotations

import csv
import json
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "crudos"
SEMILLA = 2026
INICIO = date(2025, 12, 1)
FIN = date(2026, 11, 30)

CIUDADES = {
    "Lebrija": 30,
    "Bucaramanga": 24,
    "San Gil": 9,
    "Girón": 8,
    "Floridablanca": 8,
    "Piedecuesta": 6,
    "Bogotá": 7,
    "Medellín": 3,
    "Cúcuta": 3,
    "Barranquilla": 2,
}
VARIANTES_SUCIAS = {
    "Bogotá": ["bogota", "Bogota D.C.", " BOGOTÁ"],
    "Bucaramanga": ["bucaramanga", "B/manga", "Bucaramanga "],
    "Girón": ["Giron", "giron"],
    "San Gil": ["san gil", "SAN GIL"],
    "Medellín": ["Medellin"],
    "Cúcuta": ["Cucuta"],
    "Lebrija": ["lebrija", " Lebrija"],
}
METODOS_PAGO = {"Contraentrega": 50, "Nequi": 35, "Tarjeta (enlace)": 15}
METODOS_SUCIOS = {"Contraentrega": ["contraentrega", "Contra entrega"], "Nequi": ["NEQUI", "nequi"]}

TEMPORADA = {12: 1.8, 1: 0.7, 2: 0.8, 3: 0.9, 4: 0.9, 5: 1.1, 6: 1.25, 7: 1.0, 8: 0.9, 9: 1.1, 10: 1.0, 11: 1.35}
PEDIDOS_POR_DIA = 5.0
CRECIMIENTO_MENSUAL = 0.03
POPULARIDAD = {"Gorras": 3.0, "Pantalones": 2.2, "Pantalonetas": 1.6, "Bermudas": 1.2, "Sudaderas": 1.3, "Zapatos": 1.0}


@dataclass(frozen=True)
class Producto:
    id: str
    nombre: str
    categoria: str
    precio: int
    tallas: tuple[str, ...]


def cargar_catalogo(ruta: Path = RAIZ / "catalogo.json") -> list[Producto]:
    filas = json.loads(ruta.read_text(encoding="utf-8"))
    return [
        Producto(p["id"], p["nombre"], p["categoria"], int(p["precio"]), tuple(p.get("tallas") or ()))
        for p in filas
        if p.get("precio")
    ]


def _elegir(azar: random.Random, pesos: dict[str, float]) -> str:
    return azar.choices(list(pesos), weights=list(pesos.values()))[0]


def _ensuciar(azar: random.Random, valor: str, variantes: dict[str, list[str]], prob: float) -> str:
    if valor in variantes and azar.random() < prob:
        return azar.choice(variantes[valor])
    return valor


def generar(semilla: int = SEMILLA) -> dict[str, list[dict[str, object]]]:
    azar = random.Random(semilla)
    catalogo = cargar_catalogo()
    pesos_producto = [POPULARIDAD.get(p.categoria, 1.0) * azar.uniform(0.4, 1.6) for p in catalogo]

    clientes: list[dict[str, object]] = []
    for n in range(1, 461):
        ciudad = _elegir(azar, CIUDADES)
        if azar.random() < 0.7:
            registro = INICIO - timedelta(days=azar.randint(1, 365))
        else:
            registro = INICIO + timedelta(days=azar.randint(0, (FIN - INICIO).days))
        clientes.append(
            {
                "cliente_id": f"C{n:04d}",
                "ciudad": _ensuciar(azar, ciudad, VARIANTES_SUCIAS, 0.25),
                "fecha_registro": registro.isoformat(),
                "canal_registro": azar.choices(["web", "whatsapp"], weights=[60, 40])[0],
            }
        )
    pesos_cliente = [azar.paretovariate(1.6) for _ in clientes]

    pedidos: list[dict[str, object]] = []
    items: list[dict[str, object]] = []
    numero = 1001
    dia = INICIO
    mes_indice = 0
    while dia <= FIN:
        mes_indice = (dia.year - INICIO.year) * 12 + dia.month - INICIO.month
        esperado = PEDIDOS_POR_DIA * TEMPORADA[dia.month] * (1 + CRECIMIENTO_MENSUAL) ** mes_indice
        if dia.weekday() >= 5:
            esperado *= 1.3
        for _ in range(max(0, round(azar.gauss(esperado, esperado**0.5)))):
            cliente = azar.choices(clientes, weights=pesos_cliente)[0]
            if str(cliente["fecha_registro"]) > dia.isoformat():
                continue
            hora = datetime(dia.year, dia.month, dia.day, azar.choice(range(8, 22)), azar.randint(0, 59))
            por_mayor = azar.random() < 0.08
            antiguedad = (FIN - dia).days
            if antiguedad > 12:
                estado = azar.choices(["entregado", "cancelado"], weights=[91, 9])[0]
            else:
                estado = azar.choice(["nuevo", "confirmado", "enviado", "entregado", "cancelado"])
            pedido_id = f"VS-{numero}"
            numero += 1
            pedidos.append(
                {
                    "pedido_id": pedido_id,
                    "cliente_id": cliente["cliente_id"],
                    "fecha_pedido": hora.isoformat(sep=" "),
                    "estado": estado,
                    "metodo_pago": _ensuciar(azar, _elegir(azar, METODOS_PAGO), METODOS_SUCIOS, 0.15),
                    "tipo_venta": "mayor" if por_mayor else "detal",
                }
            )
            elegidos = azar.choices(
                catalogo, weights=pesos_producto, k=azar.choices([1, 2, 3], weights=[62, 28, 10])[0]
            )
            for producto in {p.id: p for p in elegidos}.values():
                items.append(
                    {
                        "pedido_id": pedido_id,
                        "producto_id": producto.id,
                        "talla": azar.choice(producto.tallas) if producto.tallas else "",
                        "cantidad": azar.randint(6, 12) if por_mayor else azar.choices([1, 2], weights=[88, 12])[0],
                        "precio_unitario": producto.precio,
                    }
                )
        dia += timedelta(days=1)

    productos = [
        {
            "producto_id": p.id,
            "nombre": p.nombre,
            "categoria": p.categoria,
            "precio": p.precio,
            "tallas": "|".join(p.tallas),
        }
        for p in catalogo
    ]
    return {"productos": productos, "clientes": clientes, "pedidos": pedidos, "items_pedido": items}


def escribir(tablas: dict[str, list[dict[str, object]]], carpeta: Path = SALIDA) -> None:
    carpeta.mkdir(parents=True, exist_ok=True)
    for nombre, filas in tablas.items():
        with (carpeta / f"{nombre}.csv").open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
            escritor.writeheader()
            escritor.writerows(filas)


if __name__ == "__main__":
    datos = generar()
    escribir(datos)
    for nombre, filas in datos.items():
        print(f"{nombre}: {len(filas)} filas")
