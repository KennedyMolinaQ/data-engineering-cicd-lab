# 10 · Scripts de automatización

"Un comando para cada cosa". Hay versión PowerShell (`.ps1`, Windows) y Bash (`.sh`).
Ejecutar siempre **desde la raíz del repositorio**.

| Script | Propósito |
|--------|-----------|
| `setup` | Crea el entorno virtual e instala dependencias. |
| `run-tests` | Lint (Ruff) + formato (Black) + pytest con cobertura + checklist. |
| `run-local` | Ejecuta el pipeline con Spark local. |
| `deploy` | Valida, despliega y ejecuta el bundle. Uso: `deploy dev\|prod`. |
| `clean` | Limpia caches y artefactos generados. |
| `check_best_practices.py` | Checklist de buenas prácticas (usado por `run-tests` y CI). |

## Ejemplos

```powershell
# Windows
.\10-automation-scripts\setup.ps1
.\10-automation-scripts\run-tests.ps1
.\10-automation-scripts\deploy.ps1 dev
```

```bash
# Linux/Mac
./10-automation-scripts/setup.sh
./10-automation-scripts/run-tests.sh
./10-automation-scripts/deploy.sh dev
```
