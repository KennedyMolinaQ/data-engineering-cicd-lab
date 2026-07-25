"""Pruebas del orquestador ``jobs.ventas_diarias.run()`` con dobles de prueba.

IMPORTANTE (honestidad sobre PySpark): ``jobs/ventas_diarias.py`` importa
``pyspark.sql.functions`` a NIVEL DE MÓDULO (para construir la constante
``_CONDICION_FILA_VALIDA``), así que este archivo necesita PySpark instalado
únicamente para poder **importar** el módulo bajo prueba, no para ejecutar
Spark de verdad. Todas las dependencias reales de Spark (``obtener_spark``,
``leer_csv``, ``transformar_ventas``) se sustituyen por dobles (fakes)
simples que no requieren un cluster ni una SparkSession real.

Verificado empíricamente en este entorno (sin PySpark instalado en el
``.venv`` del proyecto): intentar `import jobs.ventas_diarias` falla con
``ModuleNotFoundError: No module named 'pyspark'``. Por eso este archivo usa
``pytest.importorskip("pyspark")`` para saltarse limpiamente aquí y queda
listo para ejecutarse en CI (donde sí está instalado PySpark).
"""

from __future__ import annotations

import pytest

pytest.importorskip(
    "pyspark",
    reason="jobs.ventas_diarias importa pyspark.sql.functions a nivel de módulo",
)

import jobs.ventas_diarias as job  # noqa: E402
from common.validaciones import COLUMNAS_ESPERADAS  # noqa: E402


class FakeDataFrame:
    """Doble mínimo que soporta los métodos que invoca ``run()``.

    No evalúa condiciones de Spark de verdad: ``filter`` simplemente ignora
    la condición recibida y devuelve otro fake con el conteo configurado.
    Esto es intencional y suficiente para probar el FLUJO de control de
    ``run()`` (orden de llamadas, propagación de errores, valor de retorno);
    la corrección de la condición de filtrado en sí (cantidad>0 y
    precio_unitario>=0) se prueba con Spark real en las pruebas de
    integración (``test_pipeline_ventas.py``), no aquí.
    """

    def __init__(self, columns: list[str], count_valor: int = 0) -> None:
        self.columns = columns
        self._count_valor = count_valor
        self.cache_llamado = False
        self.unpersist_llamado = False
        self.show_llamado = False

    def cache(self) -> FakeDataFrame:
        self.cache_llamado = True
        return self

    def filter(self, _condicion: object) -> FakeDataFrame:
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
        columnas_incompletas = ["id_venta", "fecha", "producto"]
        fake_df = FakeDataFrame(columns=columnas_incompletas)

        monkeypatch.setattr(job, "obtener_spark", lambda app_name: object())
        monkeypatch.setattr(job, "leer_csv", lambda spark, ruta: fake_df)
        monkeypatch.setattr(
            job,
            "transformar_ventas",
            lambda df: pytest.fail("transformar_ventas no debería llamarse si faltan columnas"),
        )

        with pytest.raises(ValueError, match="Faltan columnas"):
            job.run(ruta_csv="ruta/no/usada.csv")


class TestRunCaminoFeliz:
    def test_retorna_numero_de_filas_procesadas(self, monkeypatch: pytest.MonkeyPatch) -> None:
        fake_ventas = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=10)
        # Dos filas descartadas por la condición de validación (cantidad<=0 o
        # precio_unitario<0): 10 leídas, 8 válidas.
        fake_ventas_validas = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=8)
        fake_resultado = FakeDataFrame(columns=[*COLUMNAS_ESPERADAS, "importe_total", "categoria"])
        fake_resultado._count_valor = 8

        monkeypatch.setattr(fake_ventas, "filter", lambda _condicion: fake_ventas_validas)
        monkeypatch.setattr(job, "obtener_spark", lambda app_name: object())
        monkeypatch.setattr(job, "leer_csv", lambda spark, ruta: fake_ventas)
        monkeypatch.setattr(job, "transformar_ventas", lambda df: fake_resultado)

        total = job.run(ruta_csv="ruta/no/usada.csv")

        assert total == 8
        assert fake_ventas.cache_llamado is True
        assert fake_ventas.unpersist_llamado is True
        assert fake_resultado.show_llamado is True

    def test_usa_ruta_csv_indicada_al_leer(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """``run(ruta_csv=...)`` debe propagar la ruta recibida a ``leer_csv``."""
        fake_ventas = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=1)
        monkeypatch.setattr(fake_ventas, "filter", lambda _condicion: fake_ventas)
        fake_resultado = FakeDataFrame(columns=list(COLUMNAS_ESPERADAS), count_valor=1)

        rutas_recibidas: list[str] = []

        def fake_leer_csv(spark: object, ruta: str) -> FakeDataFrame:
            rutas_recibidas.append(ruta)
            return fake_ventas

        monkeypatch.setattr(job, "obtener_spark", lambda app_name: object())
        monkeypatch.setattr(job, "leer_csv", fake_leer_csv)
        monkeypatch.setattr(job, "transformar_ventas", lambda df: fake_resultado)

        job.run(ruta_csv="mi/ruta/personalizada.csv")

        assert rutas_recibidas == ["mi/ruta/personalizada.csv"]
