-- Incluye cancelados: sirve para medir la tasa de cancelación por método de pago.
select
    metodo_pago,
    count(distinct pedido_id) as pedidos,
    count(distinct case when estado = 'cancelado' then pedido_id end) as cancelados,
    round(100.0 * count(distinct case when estado = 'cancelado' then pedido_id end)
          / count(distinct pedido_id), 1) as cancelacion_pct
from {{ ref('fct_ventas') }}
group by metodo_pago
order by pedidos desc
