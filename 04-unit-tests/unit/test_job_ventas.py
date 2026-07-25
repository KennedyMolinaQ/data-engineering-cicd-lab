"""Pruebas del orquestador ``jobs.ventas_diarias.run()`` con dobles de prueba.

``run()`` orquesta llamadas a la capa Spark (``obtener_spark``, ``leer_csv``,
``filtrar_filas_validas``, ``transformar_ventas``). Aquí se sustituyen todas por
dobles (fakes) simples, de modo que NO se necesita un ``SparkContext`` activo ni
una SparkSession real: se prueba el FLUJO de control (orden de llamadas,
propagación de errores, valor de retorno), no la lógica de Spark en sí (esa se
cubre en ``test_pipeline_ventas.py`` con Spark real).

``jobs/ventas_diarias.py`` importa ``utilities`` (que a su vez importa PySpark),
así que importar el módulo bajo prueba requiere que PySpark esté instalado —pero
NO que haya una sesión activa, porque ya no se construye ninguna expresión de
Spark a nivel de módulo—. En el ``.venv`` local sin PySpark, ``importorskip``
salta este archivo; en CI (con PySpark) se ejecuta con los dobles.
"""

from __future__ import annotations

import pytest

pytest.importorskip(
    "pyspark",
    reason="jobs.ventas_diarias importa utilities, que depende de PySpark",
)

import jobs.ventas_diarias as job  # noqa: E402
from common.validaciones import COLUMNAS_ESPERADAS  # noqa: E402


class FakeDataFrame:
    """Doble mínimo que soporta los métodos que invoca ``run()``."""

    def __init__(self, columns: list[str], count_valor: int = 0) -> None:
        self.columns = columns
        self._count_valor = count_valor
        self.cache_llamado = False
        self.unpersist_llamado = False
        self.show_llamado = False

    def cache(self) -> FakeDataFrame:
        self.cache_llamado = True
        return self

    def count(self) -> int:
        return self._count_valor

    def unpersist(self) -> FakeDataFrame:
        self.unpersist_llamado = True
        return self

    def show(self, *args: object, **kwargs: object) -> None:
        self.show_llamado = True


class TestRunColumnasFaltantes:
    def test_lanza_value_error_si_faltan_columnas(self, monkeypatch: pytest.MonkeyPatch) -> None:
        fake_df = FakeDataFrame(columns=["id_venta", "fecha", "producto"])

        monkeypatch.setattr(job, "obtener_spark", lambda app_name: object())
        monkeypatch.setattr(job, "leer_csv", lambda spark, ruta: fake_df)
        monkeypatch.setattr(
            job,
            "filtrar_filas_validas",
            lambda df: pytest.fail("filtrar_filas_validas no debería llamarse si faltan columnas"),
        )
        monkeypatch.setattr(
            job,
            "transformar_ventas",
            lambda df: pytest.fail("transformar_ventas no debería llamarse si faltan columnas"),
        )

        with pytest.raises(ValueError, match="Faltan columnas"):
            job.run(ruta_csv="ruta/no/usada.csv")


class TestRunCaminoFeliz:
    def test_retorna_numero_de_filas_procesadas(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # 10 filas leídas, 8 válidas tras el filtrado.
        fake_ventas = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=10)
        fake_ventas_validas = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=8)
        fake_resultado = FakeDataFrame(
            columns=[*COLUMNAS_ESPERADAS, "importe_total", "categoria"], count_valor=8
        )

        monkeypatch.setattr(job, "obtener_spark", lambda app_name: object())
        monkeypatch.setattr(job, "leer_csv", lambda spark, ruta: fake_ventas)
        monkeypatch.setattr(job, "filtrar_filas_validas", lambda df: fake_ventas_validas)
        monkeypatch.setattr(job, "transformar_ventas", lambda df: fake_resultado)

        total = job.run(ruta_csv="ruta/no/usada.csv")

        assert total == 8
        assert fake_ventas.cache_llamado is True
        assert fake_ventas.unpersist_llamado is True
        assert fake_resultado.show_llamado is True

    def test_usa_ruta_csv_indicada_al_leer(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """``run(ruta_csv=...)`` debe propagar la ruta recibida a ``leer_csv``."""
        fake_ventas = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=1)
        fake_resultado = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=1)
        rutas_recibidas: list[str] = []

        def fake_leer_csv(spark: object, ruta: str) -> FakeDataFrame:
            rutas_recibidas.append(ruta)
            return fake_ventas

        monkeypatch.setattr(job, "obtener_spark", lambda app_name: object())
        monkeypatch.setattr(job, "leer_csv", fake_leer_csv)
        monkeypatch.setattr(job, "filtrar_filas_validas", lambda df: fake_ventas)
        monkeypatch.setattr(job, "transformar_ventas", lambda df: fake_resultado)

        job.run(ruta_csv="mi/ruta/personalizada.csv")

        assert rutas_recibidas == ["mi/ruta/personalizada.csv"]
