import sys
from pathlib import Path

import pytest
from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture(scope="session")
def spark():
    # Spark puro (sem Delta): os testes cobrem a lógica de transformação/qualidade
    s = (
        SparkSession.builder.master("local[2]")
        .appName("tests")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    s.sparkContext.setLogLevel("ERROR")
    yield s
    s.stop()


@pytest.fixture(scope="session")
def sample_file():
    return ROOT / "data" / "sample" / "ca-sample.csv"
