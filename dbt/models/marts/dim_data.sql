with limites as (
    select min(data_coleta) as ini, max(data_coleta) as fim from {{ ref('stg_precos') }}
)
select
    cast(d as date)                        as data,
    year(d)                                as ano,
    month(d)                               as mes,
    strftime(d, '%Y-%m')                   as ano_mes,
    case when month(d) <= 6 then 1 else 2 end as semestre,
    dayofweek(d)                           as dia_semana
from limites, generate_series(ini, fim, interval 1 day) as t(d)
