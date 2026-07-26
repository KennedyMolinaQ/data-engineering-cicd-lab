"""Constantes del dominio (valores estables, no configurables por entorno)."""

from __future__ import annotations

# Nombre lógico de la tabla destino.
TABLA_VENTAS = "ventas_procesadas"

# Columnas derivadas que añade el pipeline.
COLUMNA_IMPORTE = "importe_total"
COLUMNA_CATEGORIA = "categoria"

# Países soportados en los datos de muestra.
PAISES = ("PE", "CL", "CO")
