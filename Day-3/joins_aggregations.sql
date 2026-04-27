-- COUNT orders per user
SELECT user_id, COUNT(*) total_orders
FROM orders
GROUP BY user_id;

-- AVG price per category
SELECT category, AVG(price)
FROM products
GROUP BY category
HAVING AVG(price) > 5000;

-- INNER JOIN
SELECT u.name,o.order_id
FROM users u
INNER JOIN orders o ON u.user_id=o.user_id;

-- LEFT JOIN
SELECT u.name,o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id=o.user_id;

-- RIGHT JOIN
SELECT u.name,o.order_id
FROM users u
RIGHT JOIN orders o ON u.user_id=o.user_id;

-- FULL JOIN
SELECT u.name,o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id=o.user_id
UNION
SELECT u.name,o.order_id
FROM users u
RIGHT JOIN orders o ON u.user_id=o.user_id;

-- SELF JOIN
SELECT a.name AS User1,b.name AS User2
FROM users a, users b
WHERE a.city=b.city AND a.user_id<>b.user_id;
