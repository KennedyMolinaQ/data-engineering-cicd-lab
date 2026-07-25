#!/usr/bin/env bash
# Calidad + pruebas (equivalente a lo que corre CI). Ejecutar desde la raíz del repo.
set -euo pipefail

echo "==> Ruff (lint)"
ruff check .

echo "==> Black (format check)"
black --check .

echo "==> pytest + cobertura (common >= 90%)"
pytest --cov=common --cov-report=term-missing --cov-fail-under=90

echo "==> Checklist de buenas practicas"
python 10-automation-scripts/check_best_practices.py

echo "OK: todas las validaciones pasaron."
