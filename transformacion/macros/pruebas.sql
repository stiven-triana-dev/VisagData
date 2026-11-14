{# Pruebas genéricas propias (sin depender de paquetes externos). #}

{% test mayor_que_cero(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}

{% test unique_combinacion(model, columnas) %}
select {{ columnas | join(', ') }}, count(*) as veces
from {{ model }}
group by {{ columnas | join(', ') }}
having count(*) > 1
{% endtest %}
