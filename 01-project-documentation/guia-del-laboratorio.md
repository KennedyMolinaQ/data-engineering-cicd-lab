# Guía del laboratorio

Recorrido paso a paso. Cada módulo construye sobre el anterior.

## Módulo 1 · Control de versiones

Objetivo: dominar branches, Pull Requests y Git Flow.

```bash
git checkout -b develop
git checkout -b feature/mi-primera-feature
# ...cambios...
git push -u origin feature/mi-primera-feature   # abre un PR hacia develop
```

- `feature/*` → PR → `develop` → `main`.
- Configura *branch protection* en `develop` y `main` (PR obligatorio + checks en verde).
- Detalle: [`adr/0001-estrategia-de-ramas.md`](adr/0001-estrategia-de-ramas.md).

## Módulo 2 · Desarrollo (Python + PySpark)

El código vive en `03-data-pipeline/src/` con capas:

- `common/` — lógica **pura** de negocio (testeable sin Spark).
- `utilities/` — helpers de Spark (sesión, I/O, transformaciones).
- `jobs/` — puntos de entrada orquestables.
- `notebooks/` — notebooks Databricks versionables.

```bash
python 03-data-pipeline/src/jobs/ventas_diarias.py
```

## Módulo 3 · Calidad

```bash
ruff check .        # linting
black --check .     # formato
pytest              # pruebas
```

Umbral de cobertura sobre `common/`: **≥ 90 %**. Ver `05-code-quality/`.

## Módulo 4 · CI

Al abrir un PR, `.github/workflows/pull-request-validation.yml` ejecuta
automáticamente: instalación de dependencias, Ruff, Black, pytest + cobertura,
checklist de buenas prácticas y validación del bundle.

## Módulo 5 · CD

- Merge a `develop` → deploy a Databricks `dev` + ejecución del Job.
- Merge a `main` → validaciones finales, deploy a `prod`, ejecución y artefactos.

Requiere configurar los *GitHub Environments* `dev` y `prod` con
`DATABRICKS_HOST` y `DATABRICKS_TOKEN`.

## Módulo 6 · Documentación

Cada carpeta tiene su `README.md`. La arquitectura y las decisiones están en
`01-project-documentation/`. Los diagramas se mantienen en Mermaid.

## Checklist de finalización

- [ ] `ruff check .` sin errores.
- [ ] `black --check .` sin cambios.
- [ ] `pytest` en verde y cobertura ≥ 90 %.
- [ ] `python 10-automation-scripts/check_best_practices.py` pasa.
- [ ] `databricks bundle validate --target dev` válido.
- [ ] PR abierto con la plantilla y checks en verde.
