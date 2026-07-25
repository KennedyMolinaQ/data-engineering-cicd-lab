# 07 · GitHub Actions

Documentación de los pipelines de CI/CD. Los **workflows ejecutables** viven en
`.github/workflows/` porque GitHub lo exige para poder correrlos.

## Workflows

| Workflow | Disparador | Qué hace |
|----------|-----------|----------|
| [`pull-request-validation.yml`](../.github/workflows/pull-request-validation.yml) | PR hacia `develop`/`main` | Lint, format, tests, cobertura, checklist, `bundle validate`. **No despliega.** |
| [`continuous-integration.yml`](../.github/workflows/continuous-integration.yml) | push a `develop` | Reusa la validación, despliega a `dev` y ejecuta el job. |
| [`continuous-deployment.yml`](../.github/workflows/continuous-deployment.yml) | push a `main` | Validaciones finales, deploy a `prod`, ejecuta el pipeline, publica artefactos. |

## Flujo

```
PR abierto ─▶ pull-request-validation ─▶ (verde) ─▶ merge a develop
   └▶ continuous-integration ─▶ deploy dev + run
       └▶ merge a main ─▶ continuous-deployment ─▶ deploy prod + artefactos
```

## Configuración de secretos

- **`DATABRICKS_HOST`** y **`DATABRICKS_TOKEN`**: se configuran como **secretos de
  repositorio u organización** (`Settings → Secrets and variables → Actions →
  Repository secrets`, o de organización), **NO** como *Environment secrets*. Motivo:
  `continuous-integration.yml` y `continuous-deployment.yml` invocan
  `pull-request-validation.yml` con `uses:` (workflow reutilizable vía `workflow_call`),
  y un job que solo hace `uses:` no admite la clave `environment:`, por lo que no puede
  resolver *Environment secrets* para reenviarlos. Los jobs `validate` de ambos
  workflows reenvían estos secretos explícitamente en su bloque `secrets:` (en vez de
  `secrets: inherit`, por mínimo privilegio); el `environment:` (`dev`/`prod`) se aplica
  dentro de los jobs concretos (`bundle-validate`, `bundle-validate-prod`, `deploy-dev`,
  `deploy-prod`) que sí lo declaran.

  > ⚠️ **No dupliques estos secretos dentro de los Environments `dev`/`prod`** de
  > GitHub. Si además existieran `DATABRICKS_HOST`/`DATABRICKS_TOKEN` como *Environment
  > secrets*, los jobs que declaran `environment:` los resolverían automáticamente y
  > podrían no coincidir con los valores reenviados por `workflow_call`, generando
  > despliegues con credenciales inconsistentes. La fuente única de verdad es siempre
  > el secreto de repositorio/organización (ver `adr/0003-gestion-de-secretos.md`).

- **`NOTIFICATION_EMAIL`**: se configura como **variable** (no secreto) del
  **Environment `prod`** (`Settings → Environments → prod → Variables`). Se inyecta en
  `continuous-deployment.yml` como `BUNDLE_VAR_notification_email`, leída
  automáticamente por el Databricks CLI como la variable `notification_email` del
  bundle.

> El entorno `prod` puede exigir *required reviewers* como gate manual antes del deploy.
