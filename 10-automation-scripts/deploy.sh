#!/usr/bin/env bash
# Valida y despliega el bundle. Uso: ./deploy.sh [dev|prod]
set -euo pipefail
TARGET="${1:-dev}"

echo "==> Validando bundle (target: $TARGET)"
databricks bundle validate --target "$TARGET"

echo "==> Desplegando (target: $TARGET)"
databricks bundle deploy --target "$TARGET"

echo "==> Ejecutando job ventas_job (target: $TARGET)"
databricks bundle run ventas_job --target "$TARGET"

echo "OK: despliegue completado."
