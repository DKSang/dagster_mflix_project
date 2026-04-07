{% macro aggregate_primary_and_list(model_name, key_col, value_col, ordinal_col, primary_alias, list_alias) %}
select
    {{ key_col }} as dlt_movie_id,
    min_by(trim({{ value_col }}), {{ ordinal_col }}) as {{ primary_alias }},
    listagg(distinct trim({{ value_col }}), ', ') within group (order by trim({{ value_col }})) as {{ list_alias }}
from {{ ref(model_name) }}
where nullif(trim({{ value_col }}), '') is not null
group by 1
{% endmacro %}

{% macro aggregate_list_only(model_name, key_col, value_col, list_alias) %}
select
    {{ key_col }} as dlt_movie_id,
    listagg(distinct trim({{ value_col }}), ', ') within group (order by trim({{ value_col }})) as {{ list_alias }}
from {{ ref(model_name) }}
where nullif(trim({{ value_col }}), '') is not null
group by 1
{% endmacro %}
