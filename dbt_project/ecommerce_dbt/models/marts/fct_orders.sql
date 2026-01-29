{{ config(materialized='incremental', unique_key='order_id') }}

SELECT
  o.order_id,
  o.user_id,
  o.product_id,
  o.amount
FROM {{ ref('stg_orders') }} o

{% if is_incremental() %}
WHERE o.order_id > (SELECT max(order_id) FROM {{ this }})
{% endif %}
