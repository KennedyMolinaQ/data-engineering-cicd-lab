"""Fixtures compartidas de pytest.

Provee una SparkSession local reutilizable para las pruebas de integración.
Las pruebas unitarias no la usan (no dependen de Spark).
"""

from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def spark():
    """SparkSession local de alcance de sesión (se crea una sola vez)."""
    pyspark = pytest.importorskip("pyspark", reason="PySpark no está instalado")
    spark = (
        pyspark.sql.SparkSession.builder.appName("tests")
        .master("local[1]")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()
