-- LGPD: a chave da revenda é um hash do CNPJ; algumas revendas são
-- empresários individuais, então o documento não é exposto na Gold.
select
    md5(cnpj_revenda)                  as revenda_sk,
    arg_max(revenda, data_coleta)      as revenda,
    arg_max(bandeira, data_coleta)     as bandeira_atual,
    arg_max(bairro, data_coleta)       as bairro,
    min(data_coleta)                   as primeira_coleta,
    max(data_coleta)                   as ultima_coleta
from {{ ref('stg_precos') }}
group by cnpj_revenda
