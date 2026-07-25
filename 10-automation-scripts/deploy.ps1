# Valida y despliega el bundle. Uso: .\deploy.ps1 [dev|prod]
$ErrorActionPreference = "Stop"
$target = if ($args.Count -ge 1) { $args[0] } else { "dev" }

Write-Host "==> Validando bundle (target: $target)" -ForegroundColor Cyan
databricks bundle validate --target $target

Write-Host "==> Desplegando (target: $target)" -ForegroundColor Cyan
databricks bundle deploy --target $target

Write-Host "==> Ejecutando job ventas_job (target: $target)" -ForegroundColor Cyan
databricks bundle run ventas_job --target $target

Write-Host "OK: despliegue completado." -ForegroundColor Green
