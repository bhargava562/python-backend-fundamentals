START TRANSACTION;

UPDATE products SET stock = stock - 1 WHERE product_id = 1;
INSERT INTO orders(user_id,order_date) VALUES (1,CURDATE());

ROLLBACK; -- undo changes

-- COMMIT example
START TRANSACTION;
UPDATE products SET stock = stock - 1 WHERE product_id = 2;
COMMIT;
