"""Lectura y escritura de datos (capa de utilidades, dependiente de PySpark)."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from utilities.esquemas import ESQUEMA_VENTAS


def leer_csv(spark: SparkSession, ruta: str, schema: StructType | None = None) -> DataFrame:
    """Lee un CSV con cabecera y esquema explícito.

    Se evita ``inferSchema`` (doble escaneo del archivo y tipos inestables
    entre ejecuciones). Si no se indica ``schema``, se usa ``ESQUEMA_VENTAS``
    por defecto.

    ``enforceSchema=false`` hace que Spark valide los nombres de la cabecera
    contra el esquema en vez de asignar los campos por posición: si alguien
    reordena o renombra columnas del CSV de origen, la lectura falla rápido en
    lugar de mezclar valores entre columnas en silencio.
    """
    return (
        spark.read.option("header", "true")
        .option("enforceSchema", "false")
        .schema(schema or ESQUEMA_VENTAS)
        .csv(ruta)
    )


def escribir_delta(df: DataFrame, ruta: str, modo: str = "overwrite") -> None:
    """Escribe un DataFrame en formato Delta en la ruta indicada."""
    df.write.format("delta").mode(modo).save(ruta)
