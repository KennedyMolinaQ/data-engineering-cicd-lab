# ADR 0003 · Gestión de secretos y configuración por entorno

- **Estado**: Aceptada
- **Fecha**: 2026-07-25

## Contexto

El proyecto maneja credenciales de Databricks y configuración que varía por entorno.
Requisito no negociable: **cero secretos en el repositorio**.

## Decisión

| Nivel | Qué | Dónde |
|-------|-----|-------|
| Local | `DATABRICKS_HOST`, token/OAuth | `.env` (gitignored) + `databricks auth login`. Plantilla en `.env.example`. |
| CI/CD | Credenciales de despliegue (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`) | **GitHub Secrets de repositorio u organización** (NO de Environment; ver aclaración abajo). |
| CI/CD | `NOTIFICATION_EMAIL` (no sensible, solo destino de alertas) | **Variable del Environment `prod`** de GitHub (`Settings > Environments > prod > Variables`). Se inyecta como `BUNDLE_VAR_notification_email` en `continuous-deployment.yml`. |
| Config no sensible | catálogo, rutas, flags | `09-configuration/settings.py` + `profiles/*.yml` (plantillas de referencia, ver aclaración abajo), ambos alimentados por variables de entorno. |

- `settings.py` **lee** de variables de entorno con defaults seguros; nunca contiene
  credenciales.
- Los secretos de deploy solo se exponen en los jobs de CD, no en la validación de PR.
- `permissions:` mínimo en cada workflow (`contents: read`).
- El entorno `prod` puede exigir *required reviewers* (gate manual) para el job de
  deploy (`environment: prod` en `continuous-deployment.yml`), aunque los secretos de
  Databricks en sí NO viven en ese Environment (ver modelo de secretos de CI/CD abajo).
- Un chequeo automático (`check_best_practices.py`) escanea patrones de secretos.

### Aclaración 1 — `09-configuration/profiles/*.yml` son plantillas, no configuración cargada

`dev.yml` y `prod.yml` son **documentación/plantillas de referencia** que muestran los
valores esperados por entorno (`catalogo`, `ruta_datos`, email de notificaciones). **No
se leen en runtime**: `settings.py` obtiene sus valores exclusivamente de variables de
entorno (`APP_ENV`, `CATALOGO`, `RUTA_DATOS`, `DATABRICKS_HOST`), nunca parseando estos
YAML. Editar `prod.yml` esperando que cambie el comportamiento del pipeline **no tiene
ningún efecto**; sirve solo como referencia legible de qué valores debería tener cada
entorno (y como documentación que `databricks.yml`/CI referencian en comentarios).

### Aclaración 2 — Modelo de secretos de CI/CD: repo/org, no Environment

Los jobs `validate` de `continuous-integration.yml` y `continuous-deployment.yml`
invocan `pull-request-validation.yml` mediante `uses:` (workflow reutilizable,
`workflow_call`). GitHub Actions **no permite** declarar `environment:` en un job que
solo hace `uses:` a otro workflow; por tanto, ese job no puede resolver *Environment
secrets* para reenviarlos al workflow llamado. Consecuencia obligada del diseño:
`DATABRICKS_HOST` y `DATABRICKS_TOKEN` deben ser **secretos de repositorio u
organización**, para que el bloque `secrets:` de esos jobs (`secrets.DATABRICKS_HOST`,
`secrets.DATABRICKS_TOKEN`) pueda leerlos y reenviarlos explícitamente vía
`workflow_call` (en vez de `secrets: inherit`, por mínimo privilegio).

> **⚠️ Advertencia (fuente única de verdad)**: NO crear secretos con los mismos nombres
> (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`) dentro de los **Environments** `dev` o `prod`
> de GitHub. Los jobs `bundle-validate` (environment `dev`) y `bundle-validate-prod`
> (environment `prod`) dentro de `pull-request-validation.yml`, así como `deploy-dev` /
> `deploy-prod`, sí declaran `environment:` — si además existieran secretos homónimos en
> esos Environments, GitHub los resolvería automáticamente en esos jobs y podrían no
> coincidir con los valores reenviados explícitamente desde el `workflow_call`,
> produciendo un despliegue con credenciales inconsistentes y difíciles de depurar. La
> única fuente de verdad para `DATABRICKS_HOST`/`DATABRICKS_TOKEN` es el secreto de
> repositorio/organización.
>
> `NOTIFICATION_EMAIL`, al no ser sensible ni requerir reenvío por `workflow_call` (solo
> se usa en el job `deploy-prod`, que sí declara `environment: prod`), se define
> correctamente como **variable** (no secreto) del Environment `prod`.

## Consecuencias

- (+) Sin credenciales versionadas; rotación sencilla (cambiar el secret en GitHub).
- (+) Los secretos de despliegue son compatibles con el patrón de workflow reutilizable
  (`workflow_call`) sin recurrir a `secrets: inherit`.
- (+) `NOTIFICATION_EMAIL` sigue aislado por entorno mediante Environment variables,
  con `required reviewers` como gate manual en `prod`.
- (−) Los secretos de Databricks pierden el aislamiento nativo por Environment que
  tendrían si el workflow no fuera reutilizable; el aislamiento dev/prod para esas
  credenciales depende de la disciplina de no duplicarlas en los Environments (ver
  advertencia arriba), no de un mecanismo de GitHub que lo impida automáticamente.
- (−) Los `profiles/*.yml` pueden inducir a error si alguien asume que se cargan en
  runtime; se documentan explícitamente como plantillas de referencia para mitigarlo.
