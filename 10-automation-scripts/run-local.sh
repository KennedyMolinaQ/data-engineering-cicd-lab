#!/usr/bin/env bash
# Ejecuta el pipeline con Spark local. Ejecutar desde la raíz del repo.
set -euo pipefail
echo "==> Ejecutando pipeline de ventas (local)"
python 03-data-pipeline/src/jobs/ventas_diarias.py
