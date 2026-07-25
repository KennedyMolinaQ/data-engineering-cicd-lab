"""Configuración central del proyecto.

Lee valores del **entorno** (variables de entorno) con defaults seguros.
NUNCA contiene credenciales: los secretos se inyectan vía variables de entorno
(local: `.env`; CI/CD: GitHub Environment secrets).
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Configuración efectiva del entorno actual."""

    entorno: str
    catalogo: str
    ruta_datos: str
    databricks_host: str | None

    @classmethod
    def cargar(cls) -> Settings:
        entorno = os.getenv("APP_ENV", "dev")
        return cls(
            entorno=entorno,
            catalogo=os.getenv("CATALOGO", entorno),
            ruta_datos=os.getenv("RUTA_DATOS", "08-sample-data/csv/ventas.csv"),
            # El host puede venir del entorno; el token NUNCA se lee/almacena aquí.
            databricks_host=os.getenv("DATABRICKS_HOST"),
        )


settings = Settings.cargar()
