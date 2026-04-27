INSERT INTO users(name,email,phone,city) VALUES
('Asha','asha@gmail.com','900000001','Chennai'),
('Ravi','ravi@gmail.com','900000002','Bangalore'),
('Kiran','kiran@gmail.com','900000003','Hyderabad'),
('Meena','meena@gmail.com','900000004','Mumbai');

INSERT INTO products(name,price,stock,category) VALUES
('Laptop',75000,10,'Electronics'),
('Headphones',2000,50,'Electronics'),
('Shoes',3000,30,'Fashion'),
('Phone',50000,15,'Electronics'),
('Watch',4000,20,'Accessories');

INSERT INTO orders(user_id,order_date,status) VALUES
(1,'2025-04-01','DELIVERED'),
(2,'2025-04-02','PLACED'),
(1,'2025-04-05','SHIPPED');

INSERT INTO order_items(order_id,product_id,quantity,price) VALUES
(1,1,1,75000),
(1,2,2,2000),
(2,3,1,3000),
(3,4,1,50000);
