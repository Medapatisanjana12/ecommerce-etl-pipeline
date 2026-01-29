-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
('Sanjana', 'sanjana@gmail.com'),
('Rahul', 'rahul@gmail.com'),
('Ananya', 'ananya@gmail.com');

-- PRODUCTS TABLE
CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL PRIMARY KEY,
  product_name VARCHAR(100),
  price NUMERIC(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (product_name, price) VALUES
('Laptop', 65000),
('Mobile', 25000),
('Headphones', 3000);
