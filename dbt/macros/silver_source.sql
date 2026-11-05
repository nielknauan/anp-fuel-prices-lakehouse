{# Lê a Silver gerada pelo Spark: delta_scan (padrão) ou read_parquet (fallback) #}
{% macro silver_source() %}
  {%- set path = var('silver_path') -%}
  {%- if var('silver_reader') == 'parquet' -%}
    read_parquet('{{ path }}/**/*.parquet', hive_partitioning = true)
  {%- else -%}
    delta_scan('{{ path }}')
  {%- endif -%}
{% endmacro %}

{# Gera o schema exatamente com o nome configurado (sem prefixo do target) #}
{% macro generate_schema_name(custom_schema_name, node) -%}
  {{ custom_schema_name or target.schema }}
{%- endmacro %}
