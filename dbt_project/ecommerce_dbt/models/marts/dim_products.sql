SELECT
  product_id,
  product_name,
  price
FROM {{ ref('stg_products') }}
