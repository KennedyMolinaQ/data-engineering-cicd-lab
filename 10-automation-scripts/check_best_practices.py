"""Checklist automático de buenas prácticas.

Verifica criterios del proyecto y falla (exit code 1) si alguno no se cumple.
Se ejecuta en CI y localmente:

    python 10-automation-scripts/check_best_practices.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

CARPETAS_ESPERADAS = [
    "01-project-documentation",
    "02-development-environment",
    "03-data-pipeline",
    "04-unit-tests",
    "05-code-quality",
    "06-databricks-deployment",
    "07-github-actions",
    "08-sample-data",
    "09-configuration",
    "10-automation-scripts",
    "11-project-resources",
]

# Patrones de posibles secretos filtrados.
PATRONES_SECRETOS = [
    re.compile(r"dapi[0-9a-f]{32}(-\d+)?"),  # token de Databricks (con sufijo opcional -N)
    re.compile(r"AKIA[0-9A-Z]{16}"),  # access key de AWS
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

# Prueba de integración mínima esperada para la capa utilities/ (ver punto 4
# de la auditoría de QA): debe existir al menos un test end-to-end del
# pipeline que ejercite utilities/ con una SparkSession real.
RUTA_TEST_INTEGRACION_UTILITIES = Path("04-unit-tests") / "integration" / "test_pipeline_ventas.py"


def _error(mensaje: str, fallos: list[str]) -> None:
    fallos.append(mensaje)
    print(f"  [FALLO] {mensaje}")


def verificar_estructura(fallos: list[str]) -> None:
    print("→ Estructura del proyecto")
    for carpeta in CARPETAS_ESPERADAS:
        if not (RAIZ / carpeta).is_dir():
            _error(f"Falta la carpeta {carpeta}", fallos)


def verificar_gitignore(fallos: list[str]) -> None:
    print("→ .env fuera del repositorio")
    try:
        gitignore = (RAIZ / ".gitignore").read_text(encoding="utf-8")
    except FileNotFoundError:
        _error("No se encontró .gitignore en la raíz del repositorio", fallos)
        return
    if ".env" not in gitignore:
        _error(".env no está en .gitignore", fallos)


def verificar_secretos(fallos: list[str]) -> None:
    print("→ Sin secretos en el código")
    for archivo in RAIZ.rglob("*.py"):
        if ".venv" in archivo.parts or "__pycache__" in archivo.parts:
            continue
        texto = archivo.read_text(encoding="utf-8", errors="ignore")
        for patron in PATRONES_SECRETOS:
            if patron.search(texto):
                _error(f"Posible secreto en {archivo.relative_to(RAIZ)}", fallos)


def verificar_tests_de_common(fallos: list[str]) -> None:
    print("→ Cada módulo de common tiene pruebas")
    common = RAIZ / "03-data-pipeline" / "src" / "common"
    tests = RAIZ / "04-unit-tests" / "unit"
    modulos = {p.stem for p in common.glob("*.py") if p.stem != "__init__"}
    probados = {p.stem.replace("test_", "") for p in tests.glob("test_*.py")}
    for modulo in modulos - probados:
        _error(f"El módulo common/{modulo}.py no tiene test asociado", fallos)


def verificar_prueba_integracion_utilities(fallos: list[str]) -> None:
    print("→ Existe una prueba de integración para utilities/")
    ruta = RAIZ / RUTA_TEST_INTEGRACION_UTILITIES
    if not ruta.is_file():
        _error(
            f"No existe la prueba de integración esperada para utilities/: "
            f"{RUTA_TEST_INTEGRACION_UTILITIES}",
            fallos,
        )


def main() -> int:
    print("Checklist de buenas prácticas\n" + "=" * 32)
    fallos: list[str] = []
    verificar_estructura(fallos)
    verificar_gitignore(fallos)
    verificar_secretos(fallos)
    verificar_tests_de_common(fallos)
    verificar_prueba_integracion_utilities(fallos)

    print("=" * 32)
    if fallos:
        print(f"❌ {len(fallos)} problema(s) encontrados.")
        return 1
    print("✅ Todas las verificaciones pasaron.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
