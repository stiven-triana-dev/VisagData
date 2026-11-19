with directo as (
    select sum(i.cantidad * i.precio_unitario) as total
    from {{ ref('stg_items_pedido') }} i
    join {{ ref('stg_pedidos') }} p using (pedido_id)
    where p.estado <> 'cancelado'
),
modelo as (
    select sum(ingreso) as total from {{ ref('fct_ventas') }} where es_venta
)
select directo.total as total_directo, modelo.total as total_modelo
from directo, modelo
where directo.total <> modelo.total
