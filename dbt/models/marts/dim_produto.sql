select
    md5(produto)   as produto_sk,
    produto,
    case
        when produto like 'GASOLINA%' then 'GASOLINA'
        when produto like 'DIESEL%'   then 'DIESEL'
        else produto
    end            as grupo_produto,
    any_value(unidade_medida) as unidade_medida
from {{ ref('stg_precos') }}
group by produto
