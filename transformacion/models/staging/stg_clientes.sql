-- La ciudad llega escrita de muchas formas ("bogota", " BOGOTÁ", "B/manga"...):
-- se normaliza (minúsculas, sin tildes ni espacios sobrantes) y se cruza con el diccionario.
with clientes as (
    select
        cliente_id,
        lower(strip_accents(trim(ciudad))) as clave_ciudad,
        cast(fecha_registro as date)       as fecha_registro,
        lower(trim(canal_registro))        as canal_registro
    from {{ source('crudos', 'clientes') }}
)

select
    c.cliente_id,
    d.ciudad,
    d.departamento,
    c.fecha_registro,
    c.canal_registro
from clientes c
left join {{ ref('ciudades') }} d on d.clave = c.clave_ciudad
