with ventas as (
    select producto_id, sum(cantidad) as unidades, sum(ingreso) as ingresos
    from {{ ref('fct_ventas') }}
    where es_venta
    group by producto_id
)

select
    p.producto_id,
    p.producto,
    p.categoria,
    p.precio,
    p.numero_tallas,
    coalesce(v.unidades, 0) as unidades_vendidas,
    coalesce(v.ingresos, 0) as ingresos
from {{ ref('stg_productos') }} p
left join ventas v using (producto_id)
