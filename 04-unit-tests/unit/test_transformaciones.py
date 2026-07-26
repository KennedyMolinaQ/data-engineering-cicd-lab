"""Pruebas unitarias de la lógica pura (sin Spark)."""

import pytest

from common.transformaciones import (
    calcular_importe,
    categorizar_importe,
    normalizar_texto,
)


class TestCalcularImporte:
    def test_calculo_basico(self) -> None:
        assert calcular_importe(2, 25.50) == 51.00

    def test_redondea_a_dos_decimales(self) -> None:
        assert calcular_importe(3, 8.333) == 25.00

    def test_cantidad_cero(self) -> None:
        assert calcular_importe(0, 10.0) == 0.0

    def test_cantidad_negativa_falla(self) -> None:
        with pytest.raises(ValueError, match="cantidad"):
            calcular_importe(-1, 10.0)

    def test_precio_negativo_falla(self) -> None:
        with pytest.raises(ValueError, match="precio"):
            calcular_importe(1, -5.0)


class TestCategorizarImporte:
    @pytest.mark.parametrize(
        ("importe", "esperado"),
        [
            (200.0, "alto"),
            (100.0, "alto"),  # límite inferior de 'alto'
            (99.99, "medio"),
            (30.0, "medio"),  # límite inferior de 'medio'
            (29.99, "bajo"),
            (0.0, "bajo"),
        ],
    )
    def test_umbrales(self, importe: float, esperado: str) -> None:
        assert categorizar_importe(importe) == esperado


class TestNormalizarTexto:
    def test_colapsa_espacios_y_capitaliza(self) -> None:
        assert normalizar_texto("  teclado   mecanico ") == "Teclado Mecanico"

    def test_texto_simple(self) -> None:
        assert normalizar_texto("monitor") == "Monitor"
