# Limpia caches y artefactos generados. Ejecutar desde la raíz del repo.
$ErrorActionPreference = "SilentlyContinue"
Write-Host "==> Limpiando caches y artefactos" -ForegroundColor Cyan
Get-ChildItem -Path . -Include __pycache__,.pytest_cache,.ruff_cache -Recurse -Directory |
    Remove-Item -Recurse -Force
Remove-Item -Force .coverage, coverage.xml
Remove-Item -Recurse -Force spark-warehouse, metastore_db, derby.log
Write-Host "OK: limpieza completada." -ForegroundColor Green
