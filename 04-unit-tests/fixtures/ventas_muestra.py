"""Datos de prueba deterministas para las pruebas de integración."""

from __future__ import annotations

# Filas crudas de ventas (mismo esquema que 08-sample-data/csv/ventas.csv).
VENTAS_CRUDAS: list[dict[str, object]] = [
    {"id_venta": 1, "producto": "  teclado ", "cantidad": 2, "precio_unitario": 25.50},
    {"id_venta": 2, "producto": "monitor", "cantidad": 1, "precio_unitario": 200.00},
    {"id_venta": 3, "producto": "memoria usb", "cantidad": 4, "precio_unitario": 6.00},
]

# Resultado esperado tras aplicar la transformación (categoría por importe).
CATEGORIAS_ESPERADAS = {
    1: "medio",  # 51.00
    2: "alto",  # 200.00
    3: "bajo",  # 24.00
}
