# Instalación de Python

Se recomienda Python **3.11** para alinear con el runtime de Databricks.

## Windows

1. Descarga desde [python.org](https://www.python.org/downloads/) o usa `winget`:
   ```powershell
   winget install Python.Python.3.11
   ```
2. Verifica: `python --version`

## Gestión de versiones (opcional, recomendado)

Con **pyenv** puedes fijar la versión por proyecto (respeta `.python-version`):

```bash
pyenv install 3.11.9
pyenv local 3.11.9
```

## Java (requisito de PySpark)

PySpark necesita un JDK (8, 11 o 17):

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

Verifica: `java -version`
