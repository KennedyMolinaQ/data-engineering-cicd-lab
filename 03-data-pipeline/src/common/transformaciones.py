"""Lógica de negocio **pura** (sin PySpark, sin I/O).

Estas funciones definen las reglas del dominio "ventas" y se pueden probar con
`pytest` en milisegundos, sin necesidad de un cluster ni de una SparkSession.
La capa `utilities` reimplementa estas reglas con expresiones de Spark para
ejecutarlas a escala, y las pruebas de integración verifican que ambas coinciden.
"""

from __future__ import annotations

# Umbrales de categorización del importe (fuente única de verdad del dominio).
UMBRAL_IMPORTE_ALTO = 100.0
UMBRAL_IMPORTE_MEDIO = 30.0

CATEGORIA_ALTO = "alto"
CATEGORIA_MEDIO = "medio"
CATEGORIA_BAJO = "bajo"


def calcular_importe(cantidad: int, precio_unitario: float) -> float:
    """Importe total de una línea de venta = cantidad * precio_unitario.

    Redondea a 2 decimales. Lanza ``ValueError`` ante valores negativos.
    """
    if cantidad < 0:
        raise ValueError(f"La cantidad no puede ser negativa: {cantidad}")
    if precio_unitario < 0:
        raise ValueError(f"El precio unitario no puede ser negativo: {precio_unitario}")
    return round(cantidad * precio_unitario, 2)


def categorizar_importe(importe: float) -> str:
    """Clasifica un importe en 'alto', 'medio' o 'bajo' según los umbrales."""
    if importe >= UMBRAL_IMPORTE_ALTO:
        return CATEGORIA_ALTO
    if importe >= UMBRAL_IMPORTE_MEDIO:
        return CATEGORIA_MEDIO
    return CATEGORIA_BAJO


def normalizar_texto(texto: str) -> str:
    """Normaliza texto libre: colapsa espacios y aplica capitalización de título."""
    return " ".join(texto.split()).title()
