-- Insert single
INSERT INTO users(name,email) VALUES ('Test','test@gmail.com');

-- Insert multiple
INSERT INTO products(name,price,stock,category)
VALUES ('Tablet',25000,8,'Electronics'),
       ('Bag',1500,25,'Fashion');

-- Update
UPDATE products SET stock = stock - 1 WHERE product_id = 1;

-- Delete safely
DELETE FROM users WHERE user_id = 5;
