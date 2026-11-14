with por_mes as (
    select
        mes,
        count(distinct pedido_id)  as pedidos,
        sum(cantidad)              as unidades,
        sum(ingreso)               as ingresos,
        count(distinct cliente_id) as clientes
    from {{ ref('fct_ventas') }}
    where es_venta
    group by mes
)

select
    mes,
    pedidos,
    unidades,
    ingresos,
    clientes,
    cast(round(ingresos / pedidos) as integer) as ticket_promedio,
    round(100.0 * (ingresos - lag(ingresos) over (order by mes))
          / nullif(lag(ingresos) over (order by mes), 0), 1) as crecimiento_pct
from por_mes
order by mes
