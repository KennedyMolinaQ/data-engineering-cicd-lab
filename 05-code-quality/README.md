# 05 · Calidad de código

Estándares de calidad y su automatización.

## Herramientas

| Herramienta | Propósito | Comando |
|-------------|-----------|---------|
| **Ruff** | Linter (errores, imports, bugs, naming) | `ruff check .` |
| **Black** | Formateo determinista | `black --check .` |
| **pytest** | Pruebas unitarias e integración | `pytest` |
| **coverage** | Cobertura con umbral que bloquea | `pytest --cov=common` |

## Umbral de cobertura

El gate estricto (**≥ 90 %**) aplica a `common/` (la lógica pura de negocio), que es
la parte crítica y 100 % testeable sin Spark.

```bash
pytest --cov=common --cov-report=term-missing --cov-fail-under=90
```

## Checklist automático de buenas prácticas

El script [`../10-automation-scripts/check_best_practices.py`](../10-automation-scripts/check_best_practices.py)
verifica los criterios de [`checklist-buenas-practicas.md`](checklist-buenas-practicas.md)
y **falla el PR** si alguno no se cumple.

## Reportes

`reports/` guarda salidas de cobertura (ignorado por Git salvo `.gitkeep`).
