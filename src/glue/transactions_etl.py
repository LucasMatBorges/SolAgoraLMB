import sys
from datetime import date

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

BUCKET = 'solagoralmb'

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

ingestion_date = date.today().isoformat()


# 1. Ler tabelas RAW do Glue Catalog

countries_df = spark.read.format("csv")\
    .options(header=True, inferSchema=True)\
    .load(f"s3://{BUCKET}/bronze/countries/")

transactions_df = spark.read.format("csv")\
    .options(header=True, inferSchema=True)\
    .load(f"s3://{BUCKET}/bronze/transactions/")


# 2. Limpeza e transformação

transactions_df = (
    transactions_df
    .withColumn("transaction_value", F.col("transaction_value").cast("double"))
    .withColumn("transaction_date", F.to_date("transaction_date", "M/d/yy"))
    .withColumn("payment_due_date", F.to_date("payment_due_date", "M/d/yy"))
)


# 3. Enriquecimento com tabela countries

enriched_df = (
    transactions_df.alias("t")
    .join(countries_df.alias("c"), on="country_code", how="left")
)


# 4. Calcular dias atraso e flag

enriched_df = (
    enriched_df
    .withColumn(
        "days_delay",
        F.datediff(F.col("payment_due_date"), F.col("transaction_date"))
    )
    .withColumn("is_late", F.col("days_delay") > 0)
    .withColumn("ingestion_date", F.lit(ingestion_date))
)


# 5. Gravar em PARQUET particionado

output_path = f"s3://{BUCKET}/gold/transactions_country/"

(
    enriched_df
    .write
    .mode("overwrite")
    .format("parquet")
    .partitionBy("ingestion_date")
    .save(output_path)
)
