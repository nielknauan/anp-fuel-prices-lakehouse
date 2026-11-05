select distinct
    md5(uf || '|' || municipio) as localidade_sk,
    regiao_sigla,
    uf,
    municipio
from {{ ref('stg_precos') }}
