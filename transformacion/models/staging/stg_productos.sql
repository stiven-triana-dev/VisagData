select
    producto_id,
    trim(nombre)                          as producto,
    trim(categoria)                       as categoria,
    cast(precio as integer)               as precio,
    coalesce(len(string_split(nullif(tallas, ''), '|')), 0) as numero_tallas
from {{ source('crudos', 'productos') }}
