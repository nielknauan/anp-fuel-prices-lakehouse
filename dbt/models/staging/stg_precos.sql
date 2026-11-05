-- Contrato da Silver para o dbt: tipos explícitos e nomes estáveis
select
    cast(cnpj_revenda as varchar)       as cnpj_revenda,
    revenda,
    bandeira,
    regiao_sigla,
    uf,
    municipio,
    bairro,
    cep,
    produto,
    unidade_medida,
    cast(data_coleta as date)           as data_coleta,
    cast(valor_venda as decimal(10, 3)) as valor_venda,
    cast(valor_compra as decimal(10, 3)) as valor_compra
from {{ silver_source() }}
