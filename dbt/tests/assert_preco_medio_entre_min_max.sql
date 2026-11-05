-- Teste singular: média sempre entre mínimo e máximo
select *
from {{ ref('agg_preco_medio_mensal_uf') }}
where preco_medio < preco_min or preco_medio > preco_max
