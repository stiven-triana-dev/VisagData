select p.pedido_id
from {{ ref('stg_pedidos') }} p
left join {{ ref('stg_items_pedido') }} i using (pedido_id)
where i.pedido_id is null
