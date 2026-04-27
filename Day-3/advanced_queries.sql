-- SUBQUERY
SELECT name FROM users
WHERE user_id IN (SELECT user_id FROM orders);

-- CTE
WITH order_totals AS (
    SELECT order_id, SUM(price*quantity) total
    FROM order_items GROUP BY order_id
)
SELECT * FROM order_totals WHERE total > 50000;

-- WINDOW FUNCTION
SELECT product_id, price,
RANK() OVER(ORDER BY price DESC) price_rank
FROM products;
