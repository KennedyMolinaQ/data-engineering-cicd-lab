# Checklist de buenas prácticas

Criterios que revisa el gate automático (`check_best_practices.py`) y el rol
`code-reviewer`. Un PR no se mergea si alguno falla.

| # | Criterio | Cómo se valida |
|---|----------|----------------|
| 1 | **Nombres descriptivos** | Ruff `N` (pep8-naming) + revisión humana. |
| 2 | **Documentación** | Docstrings en módulos/funciones públicas. |
| 3 | **Tipado** | Anotaciones de tipos en firmas públicas. |
| 4 | **Imports ordenados** | Ruff `I` (isort). |
| 5 | **Sin duplicidad evidente** | Ruff + revisión. |
| 6 | **Secretos fuera del repo** | `.env` en `.gitignore`; escaneo de patrones de credenciales. |
| 7 | **Uso correcto de variables** | Ruff `F` (variables/imports sin uso). |
| 8 | **Estructura del proyecto** | Existen las carpetas `01`–`11`. |
| 9 | **Pruebas existentes** | Cada módulo de `common/` tiene su test asociado. |
| 10 | **Convenciones de nombres** | Ruff `N` + `ruff.toml`. |

## Ejecutar localmente

```bash
python 10-automation-scripts/check_best_practices.py
```
