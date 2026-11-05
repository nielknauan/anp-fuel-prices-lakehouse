from decimal import Decimal

from anp_lakehouse.bronze import read_raw_csv, to_bronze
from anp_lakehouse.quality import apply_quality_rules
from anp_lakehouse.silver import NATURAL_KEY, transform


def _silver(spark, sample_file):
    bronze = to_bronze(read_raw_csv(spark, [sample_file]))
    return bronze, transform(bronze)


def test_bronze_le_todas_as_linhas_e_renomeia_colunas(spark, sample_file):
    bronze = read_raw_csv(spark, [sample_file])
    assert bronze.count() == 36
    assert {"uf", "cnpj_revenda", "valor_venda", "data_coleta"} <= set(bronze.columns)


def test_encoding_latin1_preserva_acentos(spark, sample_file):
    bronze = read_raw_csv(spark, [sample_file])
    nomes = {r.revenda for r in bronze.select("revenda").collect()}
    assert "BEZERRA & MENDES COMERCIAL DE PETRÓLEO LTDA." in nomes


def test_tipagem_decimal_data_e_cnpj(spark, sample_file):
    _, silver = _silver(spark, sample_file)
    row = silver.filter("produto = 'GASOLINA ADITIVADA' AND uf = 'CE'").first()
    assert row.valor_venda == Decimal("5.699")
    assert str(row.data_coleta) == "2021-07-01"
    assert row.cnpj_revenda == "05397086000151"


def test_deduplicacao_pela_chave_natural(spark, sample_file):
    _, silver = _silver(spark, sample_file)
    assert silver.count() == 35  # 1 linha duplicada removida
    assert silver.groupBy(*NATURAL_KEY).count().filter("count > 1").count() == 0


def test_quality_manda_invalidos_para_quarentena(spark, sample_file):
    _, silver = _silver(spark, sample_file)
    valid, invalid = apply_quality_rules(silver)
    assert valid.count() == 33
    falhas = sorted(r._dq_falhas[0] for r in invalid.collect())
    assert falhas == ["preco_fora_da_faixa", "preco_nulo"]


def test_bronze_registra_arquivo_de_origem(spark, sample_file):
    bronze = to_bronze(read_raw_csv(spark, [sample_file]))
    origens = {r._source_file for r in bronze.select("_source_file").distinct().collect()}
    assert origens == {"ca-sample.csv"}
