"""Pruebas de integración: la transformación de Spark debe coincidir con la lógica pura."""

import sys
from pathlib import Path

import pytest

# fixtures/ está junto a este paquete de pruebas.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fixtures"))

from ventas_muestra import CATEGORIAS_ESPERADAS, VENTAS_CRUDAS  # noqa: E402

pytestmark = pytest.mark.integration


def test_transformar_ventas_coincide_con_logica_pura(spark) -> None:
    from utilities.transformaciones_spark import transformar_ventas

    df = spark.createDataFrame(VENTAS_CRUDAS)
    resultado = {fila["id_venta"]: fila for fila in transformar_ventas(df).collect()}

    assert len(resultado) == len(VENTAS_CRUDAS)
    for id_venta, categoria in CATEGORIAS_ESPERADAS.items():
        assert resultado[id_venta]["categoria"] == categoria

    # El producto se normaliza (sin espacios sobrantes, capitalizado).
    assert resultado[1]["producto"] == "Teclado"
    # El importe se calcula correctamente.
    assert resultado[2]["importe_total"] == 200.00


def test_transformar_ventas_con_cantidad_negativa_documenta_comportamiento_actual(spark) -> None:
    """``transformar_ventas`` NO valida valores de negocio (ver su propio
    docstring en ``utilities/transformaciones_spark.py``): esa responsabilidad
    es del filtrado previo en ``jobs.ventas_diarias.run()`` (condición
    ``cantidad > 0`` y ``precio_unitario >= 0``). Este test documenta el
    comportamiento actual si se le pasa una fila con ``cantidad`` negativa sin
    filtrar antes: el importe se calcula igualmente (puede quedar negativo) y
    se categoriza según los mismos umbrales, sin lanzar ningún error.
    """
    from utilities.transformaciones_spark import transformar_ventas

    fila_invalida = [
        {"id_venta": 99, "producto": "producto x", "cantidad": -2, "precio_unitario": 25.50}
    ]
    df = spark.createDataFrame(fila_invalida)
    resultado = transformar_ventas(df).collect()[0]

    assert resultado["importe_total"] == -51.00
    assert resultado["categoria"] == "bajo"


def test_transformar_ventas_con_precio_nulo_documenta_comportamiento_actual(spark) -> None:
    """Documenta el comportamiento de ``transformar_ventas`` cuando
    ``precio_unitario`` llega nulo (p. ej. una fila mal formada que se coló
    antes de las validaciones). En Spark SQL, cualquier operación aritmética o
    comparación con ``NULL`` propaga ``NULL``: ``importe_total`` queda nulo y
    la cascada de ``F.when(...).otherwise(...)`` cae en la rama por defecto
    ('bajo'), sin lanzar ningún error. Este resultado es la semántica conocida
    de Spark SQL para ``NULL``; no se ha podido confirmar en este entorno por
    no tener PySpark instalado, así que CI debe validarlo al ejecutar esta
    prueba con PySpark real.
    """
    from pyspark.sql.types import (
        DoubleType,
        IntegerType,
        StringType,
        StructField,
        StructType,
    )

    from utilities.transformaciones_spark import transformar_ventas

    schema = StructType(
        [
            StructField("id_venta", IntegerType(), True),
            StructField("producto", StringType(), True),
            StructField("cantidad", IntegerType(), True),
            StructField("precio_unitario", DoubleType(), True),
        ]
    )
    df = spark.createDataFrame([(100, "producto y", 3, None)], schema=schema)
    resultado = transformar_ventas(df).collect()[0]

    assert resultado["importe_total"] is None
    assert resultado["categoria"] == "bajo"
