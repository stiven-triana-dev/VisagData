select
    i.pedido_id,
    p.fecha_pedido,
    cast(p.fecha_pedido as date)                  as fecha,
    cast(date_trunc('month', p.fecha_pedido) as date) as mes,
    p.cliente_id,
    c.ciudad,
    c.departamento,
    i.producto_id,
    pr.producto,
    pr.categoria,
    i.talla,
    i.cantidad,
    i.precio_unitario,
    i.cantidad * i.precio_unitario                as ingreso,
    p.tipo_venta,
    p.metodo_pago,
    p.estado,
    p.estado <> 'cancelado'                       as es_venta
from {{ ref('stg_items_pedido') }} i
join {{ ref('stg_pedidos') }} p    on p.pedido_id = i.pedido_id
join {{ ref('stg_clientes') }} c   on c.cliente_id = p.cliente_id
join {{ ref('stg_productos') }} pr on pr.producto_id = i.producto_id
