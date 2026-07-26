# 06 · Despliegue en Databricks (Asset Bundles)

Despliegue **como código** con Databricks Asset Bundles.

## Archivos

- **`databricks.yml`** (en la **raíz** del repo) — definición del bundle y targets.
- **`resources/ventas_job.yml`** — el Job como código.

> El `databricks.yml` vive en la raíz para que el `sync` del bundle incluya el
> código de `03-data-pipeline`. Ver `../01-project-documentation/adr/0002-databricks-asset-bundles.md`.

## Comandos

```bash
# Validar (no requiere desplegar; corre también en CI)
databricks bundle validate --target dev

# Desplegar
databricks bundle deploy --target dev

# Ejecutar el job
databricks bundle run ventas_job --target dev
```

## Targets

| Target | mode | Uso |
|--------|------|-----|
| `dev` | development | Recursos prefijados por usuario, schedules en pausa. Default. |
| `prod` | production | Nombres limpios, validaciones estrictas. |

## Nota sobre Databricks Free Edition

La Free Edition usa cómputo **serverless** (por eso el job no define clusters). Si el
despliegue automatizado por token desde GitHub Actions estuviera limitado en tu cuenta,
`bundle validate` sigue corriendo en CI, y `deploy`/`run` pueden ejecutarse localmente
con OAuth (`databricks auth login`). Ver el ADR 0002.
