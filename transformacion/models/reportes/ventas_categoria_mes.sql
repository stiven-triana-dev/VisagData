select mes, categoria, sum(cantidad) as unidades, sum(ingreso) as ingresos
from {{ ref('fct_ventas') }}
where es_venta
group by mes, categoria
order by mes, ingresos desc
