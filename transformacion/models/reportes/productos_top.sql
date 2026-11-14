select
    row_number() over (order by ingresos desc, producto_id) as puesto,
    producto_id, producto, categoria, precio, unidades_vendidas, ingresos
from {{ ref('dim_productos') }}
where unidades_vendidas > 0
qualify puesto <= 20
