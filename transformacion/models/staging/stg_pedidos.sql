select
    pedido_id,
    cliente_id,
    cast(fecha_pedido as timestamp) as fecha_pedido,
    lower(trim(estado))             as estado,
    case
        when replace(lower(metodo_pago), ' ', '') = 'contraentrega' then 'Contraentrega'
        when lower(metodo_pago) = 'nequi' then 'Nequi'
        when lower(metodo_pago) like 'tarjeta%' then 'Tarjeta (enlace)'
    end                             as metodo_pago,
    lower(trim(tipo_venta))         as tipo_venta
from {{ source('crudos', 'pedidos') }}
