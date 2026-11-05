"""Orquestra landing -> bronze -> silver.

Exemplos:
    python -m anp_lakehouse.pipeline --sample
    python -m anp_lakehouse.pipeline --semesters 2025-01 2025-02
"""
from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

from .bronze import read_raw_csv, to_bronze, write_bronze
from .config import get_paths
from .ingest import copy_sample, download_semester
from .silver import run_silver
from .spark import get_spark

SAMPLE_FILE = Path(__file__).resolve().parents[2] / "data" / "sample" / "ca-sample.csv"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pipeline")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline medalhão de preços de combustíveis (ANP)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sample", action="store_true", help="usa a amostra versionada (offline)")
    group.add_argument("--semesters", nargs="+", help="semestres no formato AAAA-SS, ex: 2025-01")
    args = parser.parse_args()

    paths = get_paths()
    start = time.time()

    if args.sample:
        files = [copy_sample(SAMPLE_FILE, paths.landing)]
    else:
        files = [download_semester(s, paths.landing) for s in args.semesters]

    spark = get_spark()

    log.info("bronze: lendo %d arquivo(s)", len(files))
    write_bronze(to_bronze(read_raw_csv(spark, files)), paths.bronze)

    log.info("silver: transformando + quality checks + MERGE")
    stats = run_silver(spark, paths.bronze, paths.silver, paths.quarantine)

    log.info("concluído em %.1fs | %s", time.time() - start, stats)
    spark.stop()


if __name__ == "__main__":
    main()
