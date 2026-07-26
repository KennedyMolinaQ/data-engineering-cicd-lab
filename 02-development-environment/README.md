# 02 · Entorno de desarrollo

Todo lo necesario para reproducir el entorno local.

## Requisitos

- **Python 3.11+** (ver `.python-version`)
- **Java 8/11/17** (requerido por PySpark)
- **Git**
- **Databricks CLI** (para validar y desplegar el bundle)

## Pasos

```bash
# 1. Crear y activar entorno virtual
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r 02-development-environment/requirements.txt
pip install -r 02-development-environment/requirements-dev.txt
```

## Guías detalladas

- [Instalación de Python](setup-python.md)
- [Instalación del Databricks CLI](setup-databricks-cli.md)
- [Configuración de Git](setup-git.md)
- VS Code: ver [`vscode/settings.json`](vscode/settings.json) y [`vscode/extensions.json`](vscode/extensions.json)

## Verificación

```bash
python --version        # 3.11+
java -version           # 8/11/17
databricks --version    # CLI instalado
pytest                  # las pruebas pasan
```
