"""Regras de qualidade de dados: separa registros válidos e quarentena com o motivo."""
from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from .config import PRICE_MAX, PRICE_MIN

# nome da regra -> condição (SQL) que o registro precisa ATENDER
RULES: dict[str, str] = {
    "cnpj_invalido": "length(cnpj_revenda) = 14",
    "data_nula": "data_coleta IS NOT NULL",
    "preco_nulo": "valor_venda IS NOT NULL",
    "preco_fora_da_faixa": f"valor_venda BETWEEN {PRICE_MIN} AND {PRICE_MAX}",
    "uf_invalida": "length(uf) = 2",
    "produto_nulo": "produto IS NOT NULL AND produto <> ''",
}


def apply_quality_rules(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    failures = [
        F.when(~F.coalesce(F.expr(cond), F.lit(False)), F.lit(name))
        for name, cond in RULES.items()
    ]
    tagged = df.withColumn("_dq_falhas", F.array_compact(F.array(*failures)))

    valid = tagged.filter(F.size("_dq_falhas") == 0).drop("_dq_falhas")
    invalid = tagged.filter(F.size("_dq_falhas") > 0).withColumn(
        "_quarentena_em", F.current_timestamp()
    )
    return valid, invalid
