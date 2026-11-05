select
    md5(s.cnpj_revenda || '|' || s.produto || '|' || cast(s.data_coleta as varchar)) as coleta_sk,
    md5(s.cnpj_revenda)              as revenda_sk,
    md5(s.produto)                   as produto_sk,
    md5(s.uf || '|' || s.municipio)  as localidade_sk,
    s.data_coleta                    as data,
    s.bandeira,
    s.valor_venda,
    s.valor_compra
from {{ ref('stg_precos') }} s
