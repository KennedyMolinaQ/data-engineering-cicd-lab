# Instalación del Databricks CLI

El CLI moderno (v0.2x+) incluye soporte para **Asset Bundles**.

## Instalación

```powershell
# Windows (winget)
winget install Databricks.DatabricksCLI
```

```bash
# Linux/Mac
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```

Verifica: `databricks --version`

## Autenticación (OAuth U2M, recomendado para Free Edition)

```bash
databricks auth login --host https://<tu-workspace>.cloud.databricks.com
```

Esto abre el navegador y guarda un perfil local. Alternativamente, con token:

```bash
databricks configure --token
```

> ⚠️ Nunca guardes el token en el repositorio. En CI se usa `DATABRICKS_HOST` y
> `DATABRICKS_TOKEN` como *GitHub Secrets* del entorno correspondiente.

## Probar el bundle

```bash
databricks bundle validate --target dev
```
