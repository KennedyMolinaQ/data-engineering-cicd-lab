#!/usr/bin/env bash
# Prepara el entorno local. Ejecutar desde la raíz del repo.
set -euo pipefail

if [ ! -d ".venv" ]; then
  echo "==> Creando entorno virtual"
  python -m venv .venv
fi

echo "==> Instalando dependencias"
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r 02-development-environment/requirements.txt
./.venv/bin/python -m pip install -r 02-development-environment/requirements-dev.txt

echo "OK: entorno listo. Actívalo con 'source .venv/bin/activate'"
