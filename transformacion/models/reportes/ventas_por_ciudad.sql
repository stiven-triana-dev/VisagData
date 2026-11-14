select
    ciudad,
    departamento,
    count(distinct pedido_id)  as pedidos,
    count(distinct cliente_id) as clientes,
    sum(ingreso)               as ingresos,
    round(100.0 * sum(ingreso) / sum(sum(ingreso)) over (), 1) as participacion_pct
from {{ ref('fct_ventas') }}
where es_venta
group by ciudad, departamento
order by ingresos desc
