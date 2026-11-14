select categoria, talla, sum(cantidad) as unidades
from {{ ref('fct_ventas') }}
where es_venta
group by categoria, talla
order by categoria, unidades desc
