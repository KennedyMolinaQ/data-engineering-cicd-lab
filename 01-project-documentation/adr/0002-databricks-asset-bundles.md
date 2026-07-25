# ADR 0002 · Databricks Asset Bundles y ubicación del `databricks.yml`

- **Estado**: Aceptada
- **Fecha**: 2026-07-25

## Contexto

El despliegue debe ser "como código", reproducible y multi-entorno, sobre
**Databricks Free Edition** (cómputo serverless).

## Decisión

- Usar **Databricks Asset Bundles** con un único bundle y **targets** `dev`/`prod`.
- Ubicar `databricks.yml` en la **raíz del repositorio** (no en `06-databricks-deployment/`).
  Motivo: el `sync` del bundle sube el directorio raíz del bundle; el código a
  desplegar vive en `03-data-pipeline/`, fuera de `06-`. Con el bundle en la raíz, el
  sync incluye tanto el código como los recursos.
- Los **recursos** (jobs) se definen en `06-databricks-deployment/resources/*.yml` y se
  incluyen desde el `databricks.yml` raíz vía `include`.
- El Job usa cómputo **serverless** (sin clusters propios), acorde a Free Edition.

## Alternativas consideradas

- `databricks.yml` dentro de `06-databricks-deployment/`: más "ordenado" visualmente,
  pero el sync no incluiría `../03-data-pipeline` de forma fiable. Se descarta por
  corrección del despliegue.

## Consecuencias

- (+) Despliegue fiable; el código se sincroniza correctamente.
- (+) Mismo artefacto a cualquier target cambiando solo configuración.
- (−) Hay dos ficheros de configuración en la raíz (`pyproject.toml`, `databricks.yml`),
  algo habitual en proyectos reales.

## Riesgo abierto (a validar en el primer sprint)

La disponibilidad de **deploy automatizado por token** desde GitHub Actions puede estar
limitada según la edición/cuenta de Databricks Free Edition. Plan B: `bundle validate`
corre en CI sin workspace; `deploy`/`run` se ejecutan localmente con OAuth
(`databricks auth login`).
