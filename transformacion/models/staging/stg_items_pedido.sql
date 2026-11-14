select
    pedido_id,
    producto_id,
    coalesce(nullif(trim(cast(talla as varchar)), ''), 'Sin talla') as talla,
    cast(cantidad as integer)        as cantidad,
    cast(precio_unitario as integer) as precio_unitario
from {{ source('crudos', 'items_pedido') }}
