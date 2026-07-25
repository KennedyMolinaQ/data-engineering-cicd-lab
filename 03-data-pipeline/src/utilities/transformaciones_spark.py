"""Transformaciones a escala con PySpark.

Reimplementa con expresiones nativas de Spark (más eficientes que UDFs) el
enriquecimiento de ventas, compartiendo con ``common.transformaciones`` los
UMBRALES y las etiquetas de categoría (fuente única de verdad). Las pruebas
de integración verifican que la categorización y el importe coinciden con la
lógica pura.

Esta función NO valida negativos ni nulos: esa responsabilidad es del paso de
validación de calidad de datos del job (``common.validaciones`` + filtrado en
``jobs.ventas_diarias``), que se ejecuta ANTES de llamar a
``transformar_ventas``. Aquí se asume que ``df`` ya contiene únicamente filas
válidas.
"""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F  # noqa: N812  (alias idiomático de PySpark)

from common.transformaciones import (
    CATEGORIA_ALTO,
    CATEGORIA_BAJO,
    CATEGORIA_MEDIO,
    UMBRAL_IMPORTE_ALTO,
    UMBRAL_IMPORTE_MEDIO,
)


def transformar_ventas(df: DataFrame) -> DataFrame:
    """Enriquece el DataFrame de ventas.

    Añade:
    - ``producto`` normalizado (espacios colapsados, capitalización de título).
    - ``importe_total`` = cantidad * precio_unitario (2 decimales).
    - ``categoria`` según los umbrales del dominio.
    """
    importe = F.round(F.col("cantidad") * F.col("precio_unitario"), 2)

    return (
        df.withColumn("producto", F.initcap(F.trim(F.regexp_replace("producto", r"\s+", " "))))
        .withColumn("importe_total", importe)
        .withColumn(
            "categoria",
            F.when(F.col("importe_total") >= UMBRAL_IMPORTE_ALTO, F.lit(CATEGORIA_ALTO))
            .when(F.col("importe_total") >= UMBRAL_IMPORTE_MEDIO, F.lit(CATEGORIA_MEDIO))
            .otherwise(F.lit(CATEGORIA_BAJO)),
        )
    )


def filtrar_filas_validas(df: DataFrame) -> DataFrame:
    """Filtra filas con ``cantidad`` > 0 y ``precio_unitario`` >= 0.

    Misma regla de negocio que ``common.validaciones.validar_cantidad`` /
    ``validar_precio``, expresada como condición nativa de Spark para filtrar a
    escala. Se define aquí (capa ``utilities``, dependiente de PySpark) y NO como
    constante a nivel de módulo del job: ``F.col`` requiere un ``SparkContext``
    activo, así que construir la condición dentro de una función evita que
    importar el job falle sin una sesión de Spark iniciada.
    """
    return df.filter((F.col("cantidad") > 0) & (F.col("precio_unitario") >= 0))
