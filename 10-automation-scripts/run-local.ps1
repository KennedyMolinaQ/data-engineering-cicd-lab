# Ejecuta el pipeline con Spark local. Ejecutar desde la raíz del repo.
$ErrorActionPreference = "Stop"
Write-Host "==> Ejecutando pipeline de ventas (local)" -ForegroundColor Cyan
python 03-data-pipeline/src/jobs/ventas_diarias.py
