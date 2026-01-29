SELECT
  user_id,
  name,
  email
FROM {{ ref('stg_users') }}
