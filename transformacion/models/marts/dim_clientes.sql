with compras as (
    select
        cliente_id,
        count(distinct pedido_id) as pedidos,
        sum(ingreso)              as total_gastado,
        min(fecha)                as primer_pedido,
        max(fecha)                as ultimo_pedido
    from {{ ref('fct_ventas') }}
    where es_venta
    group by cliente_id
)

select
    c.cliente_id,
    c.ciudad,
    c.departamento,
    c.canal_registro,
    c.fecha_registro,
    k.primer_pedido,
    k.ultimo_pedido,
    coalesce(k.pedidos, 0)       as pedidos,
    coalesce(k.total_gastado, 0) as total_gastado,
    case
        when coalesce(k.pedidos, 0) = 0 then 'Sin compras'
        when k.pedidos = 1 then 'Nuevo'
        when k.pedidos <= 4 then 'Recurrente'
        else 'Frecuente'
    end as segmento
from {{ ref('stg_clientes') }} c
left join compras k using (cliente_id)
