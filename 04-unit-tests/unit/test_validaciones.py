"""Pruebas unitarias de las validaciones de calidad de datos (sin Spark)."""

import pytest

from common.validaciones import (
    COLUMNAS_ESPERADAS,
    faltan_columnas,
    validar_cantidad,
    validar_precio,
)


class TestValidarCantidad:
    def test_positiva_valida(self) -> None:
        assert validar_cantidad(3) is True

    def test_cero_invalida(self) -> None:
        assert validar_cantidad(0) is False

    def test_negativa_invalida(self) -> None:
        assert validar_cantidad(-2) is False

    def test_float_invalida(self) -> None:
        """Un float (aunque tenga valor entero) no es un ``int``: se rechaza."""
        assert validar_cantidad(3.0) is False

    @pytest.mark.parametrize("valor", [True, False])
    def test_bool_invalida(self, valor: bool) -> None:
        """``bool`` es subclase de ``int`` en Python, pero nunca es una cantidad
        válida de negocio (endurecimiento explícito en ``validar_cantidad``)."""
        assert validar_cantidad(valor) is False

    def test_string_invalida(self) -> None:
        assert validar_cantidad("3") is False

    def test_none_invalida(self) -> None:
        assert validar_cantidad(None) is False


class TestValidarPrecio:
    def test_positivo_valido(self) -> None:
        assert validar_precio(10.5) is True

    def test_cero_valido(self) -> None:
        assert validar_precio(0) is True

    def test_negativo_invalido(self) -> None:
        assert validar_precio(-1) is False

    def test_string_invalido(self) -> None:
        assert validar_precio("10") is False

    def test_none_invalido(self) -> None:
        assert validar_precio(None) is False

    @pytest.mark.parametrize("valor", [True, False])
    def test_bool_invalido(self, valor: bool) -> None:
        """``bool`` es subclase de ``int`` en Python, pero nunca es un precio
        válido de negocio (endurecimiento simétrico con ``validar_cantidad``)."""
        assert validar_precio(valor) is False


class TestFaltanColumnas:
    def test_todas_presentes(self) -> None:
        assert faltan_columnas(COLUMNAS_ESPERADAS) == []

    def test_detecta_faltantes(self) -> None:
        columnas = ["id_venta", "fecha", "producto"]
        assert "cantidad" in faltan_columnas(columnas)
        assert "pais" in faltan_columnas(columnas)

    def test_lista_vacia_devuelve_todas_las_esperadas(self) -> None:
        assert faltan_columnas([]) == list(COLUMNAS_ESPERADAS)

    def test_columnas_duplicadas_no_afectan_el_resultado(self) -> None:
        """Duplicar una columna presente no debe generar falsos negativos ni
        alterar la lista de columnas faltantes."""
        columnas = ["id_venta", "id_venta", "fecha", "producto", "cantidad"]
        assert faltan_columnas(columnas) == ["precio_unitario", "pais"]
