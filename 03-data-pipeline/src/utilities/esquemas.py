"""Esquemas explícitos de Spark para las fuentes de datos del dominio "ventas".

Declarar el esquema evita ``inferSchema`` (que escanea el archivo dos veces y
puede producir tipos distintos entre ejecuciones) y deja explícito el
contrato de columnas/tipos esperado por el pipeline.

Vive en ``utilities`` (no en ``common``) porque importa ``pyspark.sql.types``:
``common`` debe seguir siendo importable sin PySpark para las pruebas
unitarias puras.
"""

from __future__ import annotations

from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

# Esquema de la fuente de ventas (ver 08-sample-data/csv/ventas.csv).
# Las columnas coinciden con common.validaciones.COLUMNAS_ESPERADAS.
ESQUEMA_VENTAS = StructType(
    [
        StructField("id_venta", IntegerType(), nullable=False),
        StructField("fecha", DateType(), nullable=True),
        StructField("producto", StringType(), nullable=True),
        StructField("cantidad", IntegerType(), nullable=True),
        StructField("precio_unitario", DoubleType(), nullable=True),
        StructField("pais", StringType(), nullable=True),
    ]
)
