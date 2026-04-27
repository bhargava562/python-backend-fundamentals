-- BEFORE (NOT NORMALIZED)
CREATE TABLE orders_bad (
  order_id INT,
  user_name VARCHAR(100),
  product_name VARCHAR(100),
  product_price DECIMAL(10,2)
);

-- AFTER (3NF)
-- users, products, orders, order_items tables created earlier
