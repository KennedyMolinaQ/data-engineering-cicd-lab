"""Job de ventas diarias: extract -> transform -> load.

Punto de entrada orquestable. Funciona en local (con Spark instalado) y en
Databricks (como ``spark_python_task`` del Asset Bundle).

Uso local:
    python 03-data-pipeline/src/jobs/ventas_diarias.py
    python 03-data-pipeline/src/jobs/ventas_diarias.py --ruta-csv /ruta/a/otro.csv
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Permite importar 'common' y 'utilities' tanto en local como al sincronizarse a
# Databricks, sin depender de que el paquete esté instalado.
#
# En Databricks (spark_python_task serverless) el archivo se ejecuta con exec()
# y ``__file__`` NO está definido: se localiza 03-data-pipeline/src subiendo desde
# el directorio de trabajo (la raíz de archivos sincronizados del bundle). En
# local, ``__file__`` sí existe y se usa directamente.
try:
    SRC = Path(__file__).resolve().parents[1]  # .../03-data-pipeline/src
except NameError:  # Databricks serverless: sin __file__
    SRC = next(
        (
            base / "03-data-pipeline" / "src"
            for base in (Path.cwd(), *Path.cwd().parents)
            if (base / "03-data-pipeline" / "src").is_dir()
        ),
        Path.cwd(),
    )
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from common.validaciones import faltan_columnas  # noqa: E402
from utilities.io import leer_csv  # noqa: E402
from utilities.spark_session import obtener_spark  # noqa: E402
from utilities.transformaciones_spark import (  # noqa: E402
    filtrar_filas_validas,
    transformar_ventas,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("ventas_diarias")

# Ruta a los datos de muestra, relativa a la raíz del repositorio.
RUTA_VENTAS = SRC.parents[1] / "08-sample-data" / "csv" / "ventas.csv"


def run(ruta_csv: str | None = None) -> int:
    """Ejecuta el pipeline y devuelve el número de filas procesadas."""
    spark = obtener_spark("ventas-diarias")

    # Resuelve una ruta relativa a absoluta contra la raíz de archivos
    # (SRC.parents[1]): en Databricks el cwd puede no ser la raíz del bundle y
    # Spark no encontraría una ruta relativa; en local equivale a la raíz del
    # repo. Una ruta ya absoluta se respeta tal cual.
    ruta_path = Path(ruta_csv) if ruta_csv else RUTA_VENTAS
    if not ruta_path.is_absolute():
        ruta_path = SRC.parents[1] / ruta_path
    ruta = str(ruta_path)

    logger.info("Leyendo ventas desde %s", ruta)
    ventas = leer_csv(spark, ruta)

    columnas_faltantes = faltan_columnas(ventas.columns)
    if columnas_faltantes:
        logger.error("Faltan columnas obligatorias en la fuente: %s", columnas_faltantes)
        raise ValueError(
            f"Faltan columnas obligatorias en la fuente de ventas: {columnas_faltantes}"
        )

    # Se cachea porque se necesitan dos conteos (total y válidas) sobre la
    # misma lectura, para poder loggear cuántas filas inválidas se descartan.
    ventas.cache()
    ventas_validas = filtrar_filas_validas(ventas)
    filas_descartadas = ventas.count() - ventas_validas.count()
    if filas_descartadas:
        logger.warning(
            "Descartando %d filas inválidas (cantidad<=0 o precio_unitario<0)",
            filas_descartadas,
        )
    ventas.unpersist()

    resultado = transformar_ventas(ventas_validas)

    resultado.show(20, truncate=False)
    total = resultado.count()
    logger.info("Pipeline completado. Filas procesadas: %d", total)
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job de ventas diarias.")
    parser.add_argument(
        "--ruta-csv",
        dest="ruta_csv",
        default=None,
        help="Ruta al CSV de ventas de entrada (por defecto: datos de muestra del repo).",
    )
    args = parser.parse_args()
    run(ruta_csv=args.ruta_csv)
