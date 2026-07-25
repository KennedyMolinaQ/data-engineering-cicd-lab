"""Creación de la SparkSession (capa de utilidades, dependiente de PySpark)."""

from __future__ import annotations

from pyspark.sql import SparkSession


def obtener_spark(app_name: str = "ventas-pipeline") -> SparkSession:
    """Devuelve una SparkSession activa (la reutiliza si ya existe).

    En Databricks la sesión ya está provista; ``getOrCreate`` la reutiliza.
    En local levanta una sesión ligera adecuada para pruebas y ejecución.
    """
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
