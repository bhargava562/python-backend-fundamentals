-- COUNT orders per user
SELECT user_id, COUNT(*) total_orders
FROM orders
GROUP BY user_id;

-- AVG price per category
SELECT category, AVG(price)
FROM products
GROUP BY category
HAVING AVG(price) > 5000;
