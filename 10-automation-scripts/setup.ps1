# Prepara el entorno local. Ejecutar desde la raíz del repo.
$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    Write-Host "==> Creando entorno virtual" -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "==> Instalando dependencias" -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r 02-development-environment/requirements.txt
.\.venv\Scripts\python.exe -m pip install -r 02-development-environment/requirements-dev.txt

Write-Host "OK: entorno listo. Actívalo con .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
