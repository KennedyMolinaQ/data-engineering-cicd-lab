"""Validaciones **puras** de calidad de datos para el dominio "ventas".

Sin PySpark: reglas a nivel de valor/fila, fáciles de probar unitariamente.
"""

from __future__ import annotations

from collections.abc import Iterable

# Columnas mínimas que debe traer una fuente de ventas.
COLUMNAS_ESPERADAS: tuple[str, ...] = (
    "id_venta",
    "fecha",
    "producto",
    "cantidad",
    "precio_unitario",
    "pais",
)


def validar_cantidad(cantidad: int) -> bool:
    """La cantidad debe ser un entero estrictamente positivo.

    ``bool`` es subclase de ``int`` en Python (``isinstance(True, int)`` es
    ``True``), pero un booleano nunca es una cantidad válida de negocio, así
    que se rechaza explícitamente antes de comprobar el tipo.
    """
    if isinstance(cantidad, bool):
        return False
    return isinstance(cantidad, int) and cantidad > 0


def validar_precio(precio: float) -> bool:
    """El precio unitario no puede ser negativo.

    ``bool`` es subclase de ``int`` en Python, pero un booleano nunca es un
    precio válido de negocio, así que se rechaza explícitamente (simetría con
    ``validar_cantidad``).
    """
    if isinstance(precio, bool):
        return False
    return isinstance(precio, int | float) and precio >= 0


def faltan_columnas(columnas: Iterable[str]) -> list[str]:
    """Devuelve las columnas esperadas que NO están presentes en ``columnas``."""
    presentes = set(columnas)
    return [col for col in COLUMNAS_ESPERADAS if col not in presentes]
