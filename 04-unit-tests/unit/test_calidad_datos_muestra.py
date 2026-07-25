"""Pruebas de calidad de datos sobre el CSV de muestra (sin Spark).

Lee ``08-sample-data/csv/ventas.csv`` con el módulo ``csv`` estándar de Python
y valida el contrato de calidad de datos del dominio "ventas": esquema
esperado, unicidad de clave primaria, rangos válidos de valores y país dentro
del catálogo soportado. No depende de PySpark ni de red: es determinista y
usa el archivo real del repositorio como fixture.
"""

from __future__ import annotations

import csv
from pathlib import Path

from common.validaciones import faltan_columnas
from constants import PAISES

RUTA_CSV = Path(__file__).resolve().parents[2] / "08-sample-data" / "csv" / "ventas.csv"


def _leer_filas() -> list[dict[str, str]]:
    with RUTA_CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class TestEsquemaCsvMuestra:
    def test_archivo_existe(self) -> None:
        assert RUTA_CSV.is_file(), f"No se encontró el CSV de muestra en {RUTA_CSV}"

    def test_no_faltan_columnas_esperadas(self) -> None:
        with RUTA_CSV.open(encoding="utf-8", newline="") as f:
            cabecera = next(csv.reader(f))
        assert faltan_columnas(cabecera) == []

    def test_hay_al_menos_una_fila_de_datos(self) -> None:
        """Comprobación mínima de "frescura": el archivo no está vacío tras la
        cabecera (no tiene sentido validar calidad de un dataset sin filas)."""
        assert len(_leer_filas()) > 0


class TestUnicidadClavePrimaria:
    def test_id_venta_es_unico(self) -> None:
        filas = _leer_filas()
        ids = [int(fila["id_venta"]) for fila in filas]
        assert len(ids) == len(set(ids)), "Hay id_venta duplicados en el CSV de muestra"


class TestRangosValidos:
    def test_todas_las_cantidades_son_enteros_positivos(self) -> None:
        filas = _leer_filas()
        for fila in filas:
            cantidad = int(fila["cantidad"])
            assert cantidad > 0, f"id_venta={fila['id_venta']} tiene cantidad no positiva"

    def test_todos_los_precios_son_no_negativos(self) -> None:
        filas = _leer_filas()
        for fila in filas:
            precio = float(fila["precio_unitario"])
            assert precio >= 0, f"id_venta={fila['id_venta']} tiene precio_unitario negativo"

    def test_todos_los_paises_estan_en_el_catalogo_soportado(self) -> None:
        filas = _leer_filas()
        for fila in filas:
            assert (
                fila["pais"] in PAISES
            ), f"id_venta={fila['id_venta']} tiene un país fuera de PAISES: {fila['pais']!r}"
