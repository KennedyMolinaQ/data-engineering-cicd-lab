# Calidad + pruebas (equivalente a lo que corre CI). Ejecutar desde la raíz del repo.
$ErrorActionPreference = "Stop"

Write-Host "==> Ruff (lint)" -ForegroundColor Cyan
ruff check .

Write-Host "==> Black (format check)" -ForegroundColor Cyan
black --check .

Write-Host "==> pytest + cobertura (common >= 90%)" -ForegroundColor Cyan
pytest --cov=common --cov-report=term-missing --cov-fail-under=90

Write-Host "==> Checklist de buenas practicas" -ForegroundColor Cyan
python 10-automation-scripts/check_best_practices.py

Write-Host "OK: todas las validaciones pasaron." -ForegroundColor Green
