-- WHERE multiple conditions
SELECT * FROM products
WHERE price > 3000 AND category='Electronics';

-- ORDER BY
SELECT * FROM users ORDER BY created_at DESC;

-- LIMIT + OFFSET
SELECT * FROM products LIMIT 2 OFFSET 1;

-- LIKE
SELECT * FROM users WHERE name LIKE 'A%';

-- IN
SELECT * FROM users WHERE city IN ('Chennai','Mumbai');

-- BETWEEN
SELECT * FROM products WHERE price BETWEEN 2000 AND 60000;
