#!/usr/bin/env bash
# Limpia caches y artefactos generados. Ejecutar desde la raíz del repo.
set -uo pipefail
echo "==> Limpiando caches y artefactos"
find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) \
  -exec rm -rf {} + 2>/dev/null || true
rm -f .coverage coverage.xml
rm -rf spark-warehouse metastore_db derby.log
echo "OK: limpieza completada."
