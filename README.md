# data-engineering-cicd-lab

Laboratorio práctico para implementar **CI/CD de nivel profesional en Ingeniería de
Datos** usando exclusivamente herramientas gratuitas: Git + GitHub, GitHub Actions,
Python + PySpark, Databricks Free Edition y Databricks Asset Bundles.

> Sirve como **portafolio profesional**, **material educativo**, **demostración de
> buenas prácticas** y **base para futuros laboratorios**.

## Flujo que demuestra

```
Developer → GitHub → Pull Request → GitHub Actions → Validaciones
   → Deploy → Databricks → Ejecución del Job → Resultado
```

## Stack

| Área | Herramientas |
|------|--------------|
| Control de versiones | Git, GitHub (Git Flow) |
| CI/CD | GitHub Actions |
| Plataforma de datos | Databricks Free Edition |
| Despliegue | Databricks Asset Bundles |
| Lenguaje / Proceso | Python, PySpark |
| Calidad | pytest, Ruff, Black, coverage |
| Documentación | Markdown, Mermaid |

## Estructura del proyecto

| Carpeta | Contenido |
|---------|-----------|
| `01-project-documentation` | Arquitectura, diagramas, guía del laboratorio, ADRs |
| `02-development-environment` | Preparación del entorno local (Python, CLI, Git, VS Code) |
| `03-data-pipeline` | Código fuente del pipeline (jobs, notebooks, utilities, common) |
| `04-unit-tests` | Pruebas unitarias y de integración |
| `05-code-quality` | Configuración de calidad y checklist de buenas prácticas |
| `06-databricks-deployment` | Recursos del Databricks Asset Bundle |
| `07-github-actions` | Documentación de los pipelines de CI/CD |
| `08-sample-data` | Datos de ejemplo (csv, json, parquet, delta) |
| `09-configuration` | Configuración y variables por entorno |
| `10-automation-scripts` | Scripts de automatización (setup, deploy, tests) |
| `11-project-resources` | Material visual y de presentación |

> Los workflows ejecutables viven en `.github/workflows/` (requisito de GitHub).
> `databricks.yml` (raíz del Asset Bundle) vive en la raíz del repo para que el
> sync incluya el código de `03-data-pipeline`; los recursos del bundle están en
> `06-databricks-deployment/resources/`.

## Inicio rápido

```bash
# 1. Preparar entorno
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
pip install -r 02-development-environment/requirements.txt
pip install -r 02-development-environment/requirements-dev.txt

# 2. Calidad + pruebas (lo mismo que corre CI)
ruff check .
black --check .
pytest

# 3. Ejecutar el pipeline localmente
python 03-data-pipeline/src/jobs/ventas_diarias.py
```

## Documentación

- **Arquitectura completa** → [`01-project-documentation/ARQUITECTURA.md`](01-project-documentation/ARQUITECTURA.md)
- **Guía del laboratorio** → [`01-project-documentation/guia-del-laboratorio.md`](01-project-documentation/guia-del-laboratorio.md)
- **Flujo CI/CD** → [`01-project-documentation/flujo-cicd.md`](01-project-documentation/flujo-cicd.md)

## Licencia

Uso educativo.
