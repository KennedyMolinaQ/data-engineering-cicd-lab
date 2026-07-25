# Databricks notebook source
# MAGIC %md
# MAGIC # Exploración de ventas
# MAGIC Notebook de ejemplo (formato *source* `.py`, versionable en Git).
# MAGIC Reutiliza la misma lógica del pipeline para explorar los datos.

# COMMAND ----------

from utilities.io import leer_csv
from utilities.spark_session import obtener_spark
from utilities.transformaciones_spark import transformar_ventas

spark = obtener_spark("exploracion-ventas")

# COMMAND ----------

ventas = leer_csv(spark, "/dbfs/FileStore/ventas.csv")
resultado = transformar_ventas(ventas)
display(resultado)  # noqa: F821  (display lo provee el runtime de Databricks)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ventas por categoría

# COMMAND ----------

display(resultado.groupBy("categoria").count().orderBy("categoria"))  # noqa: F821
