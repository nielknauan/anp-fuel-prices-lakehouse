-- Mart de consumo para BI: preço médio/mín/máx por UF, produto e mês
select
    l.uf,
    p.produto,
    d.ano_mes,
    round(avg(f.valor_venda), 3) as preco_medio,
    min(f.valor_venda)           as preco_min,
    max(f.valor_venda)           as preco_max,
    count(*)                     as qtd_coletas,
    count(distinct f.revenda_sk) as qtd_revendas
from {{ ref('fct_preco_coleta') }} f
join {{ ref('dim_localidade') }} l using (localidade_sk)
join {{ ref('dim_produto') }}    p using (produto_sk)
join {{ ref('dim_data') }}       d using (data)
group by all
