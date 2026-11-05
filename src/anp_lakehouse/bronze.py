"""Bronze: dado bruto em Delta, tudo string, com metadados de ingestão."""
from __future__ import annotations

from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from .config import COLUMN_MAP


def read_raw_csv(spark: SparkSession, files: list[Path]) -> DataFrame:
    df = (
        spark.read.option("header", True)
        .option("sep", ";")
        .option("encoding", "ISO-8859-1")
        .option("inferSchema", False)
        .csv([str(f) for f in files])
    )
    # Padroniza nomes de colunas (snake_case) sem tipar nada ainda
    for original, new in COLUMN_MAP.items():
        if original in df.columns:
            df = df.withColumnRenamed(original, new)
    return df


def to_bronze(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("_source_file", F.col("_metadata.file_name"))
        .withColumn("_ingested_at", F.current_timestamp())
    )


def write_bronze(df: DataFrame, path: Path) -> None:
    # Idempotente por arquivo de origem: reprocessar um semestre substitui só ele
    files = [r["_source_file"] for r in df.select("_source_file").distinct().collect()]
    condition = " OR ".join(f"_source_file = '{f}'" for f in files)
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", condition)
        .option("mergeSchema", True)
        .save(str(path))
    )
