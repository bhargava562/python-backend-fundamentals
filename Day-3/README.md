# 🛒 E-Commerce SQL Learning Project

## 📌 Project Purpose

This project demonstrates practical SQL skills by designing and querying a real-world **E-commerce database**.

The goal is to practice:

* Database design & normalization
* DDL & DML operations
* Complex queries & joins
* Aggregations and analytics
* Transactions and rollback safety
* Real-world SQL workflow

This repository is structured as a **step-by-step SQL execution flow**.

---

# 🗂️ Repository Structure

| File                       | Purpose                            |
| -------------------------- | ---------------------------------- |
| schema.sql                 | Creates database and tables        |
| seed_data.sql              | Inserts initial sample data        |
| ddl_practice.sql           | Alters and modifies schema         |
| dml_practice.sql           | Insert/Update/Delete practice      |
| queries.sql                | Basic filtering and search queries |
| joins_and_aggregations.sql | Joins + GROUP BY analytics         |
| advanced_queries.sql       | Subqueries, CTEs, Window functions |
| transactions.sql           | Transaction & rollback examples    |
| normalization_examples.sql | 1NF → 3NF demonstration            |

---

# ⚙️ How To Run This Project

Run the SQL files in this exact order:

1️⃣ schema.sql
2️⃣ seed_data.sql
3️⃣ ddl_practice.sql
4️⃣ dml_practice.sql
5️⃣ queries.sql
6️⃣ joins_and_aggregations.sql
7️⃣ advanced_queries.sql
8️⃣ transactions.sql
9️⃣ normalization_examples.sql

This sequence simulates a **real production workflow**.

---

# 🧱 Step 1 — Database Creation

## File: `schema.sql`

This file builds the entire database structure.

### What happens in this step

### 1️⃣ Create Database

A new database named **ecommerce_db** is created and selected for use.

### 2️⃣ Create Users Table

Stores customer information.

Key concepts used:

* Primary Key → uniquely identifies each user
* UNIQUE → prevents duplicate email/phone
* NOT NULL → ensures required data is present
* DEFAULT timestamp → auto record creation time

Real-world meaning:
This table represents customers registering in an online store.

---

### 3️⃣ Create Products Table

Stores items available for purchase.

Key concepts used:

* CHECK constraint → prevents negative price/stock
* Category column → helps filtering & indexing

Real-world meaning:
This table acts like an Amazon product catalog.

---

### 4️⃣ Create Orders Table

Stores purchase orders created by users.

Key concepts:

* Foreign Key → connects order to a user
* Default order status → automatically “PLACED”

Real-world meaning:
Represents checkout activity.

---

### 5️⃣ Create Order Items Table

Stores items inside each order.

Why separate table?

Because:

* One order can contain many products
* One product can appear in many orders

This solves a **Many-to-Many relationship**.

---

### 6️⃣ Create Indexes

Indexes are added on:

* user email
* product category

Purpose:
Improve search speed in large databases.

---

# 🌱 Step 2 — Insert Initial Data

## File: `seed_data.sql`

This file simulates real application data.

### What happens

1️⃣ Insert Users
Creates customers from different cities.

2️⃣ Insert Products
Adds electronics, fashion and accessories.

3️⃣ Insert Orders
Simulates customers placing orders.

4️⃣ Insert Order Items
Connects orders with purchased products.

At this stage the database now contains **realistic working data**.

---

# 🧩 Step 3 — Schema Modifications

## File: `ddl_practice.sql`

Demonstrates **ALTER TABLE** operations.

### Actions performed

1️⃣ Add a new column (age)
Simulates new business requirement.

2️⃣ Modify column size
Expands category length as business grows.

3️⃣ Add CHECK constraint
Ensures users must be adults (age ≥ 18).

4️⃣ Drop column
Shows how unused fields are removed safely.

Real-world example:
Companies frequently update schemas as features evolve.

---

# ✏️ Step 4 — Data Manipulation

## File: `dml_practice.sql`

Practices changing data inside tables.

### Actions performed

1️⃣ Insert single record
Simulates new user signup.

2️⃣ Insert multiple records
Bulk product upload.

3️⃣ Update records
Reduce stock after a purchase.

4️⃣ Delete records safely
Remove unwanted test user using WHERE condition.

Important concept:
Always use WHERE when deleting/updating!

---

# 🔎 Step 5 — Filtering & Searching

## File: `queries.sql`

Demonstrates how applications retrieve data.

### Query Flow

1️⃣ Filter products by price AND category
Simulates product search filters.

2️⃣ Sort users by newest first
Used in admin dashboards.

3️⃣ Pagination using LIMIT + OFFSET
Used in product listing pages.

4️⃣ Pattern matching using LIKE
Search users by name prefix.

5️⃣ IN operator
Find users from selected cities.

6️⃣ BETWEEN operator
Find products in price range.

These are the **most used queries in real apps**.

---

# 📊 Step 6 — Joins & Aggregations

## File: `joins_aggregations.sql`

This file performs analytics and combines tables.

### Aggregation Flow

1️⃣ Count orders per user
Used to identify loyal customers.

2️⃣ Average price per category
Used for business insights.

3️⃣ HAVING clause
Filters grouped results.

---

### Join Flow

1️⃣ INNER JOIN
Shows users who placed orders.

2️⃣ LEFT JOIN
Shows all users, even those without orders.

3️⃣ RIGHT JOIN
Shows all orders even if user missing.

4️⃣ FULL OUTER JOIN
Combines LEFT + RIGHT for full dataset.

5️⃣ SELF JOIN
Finds users from same city (relationship analysis).

---

# 🚀 Step 7 — Advanced SQL

## File: `advanced_queries.sql`

Introduces powerful SQL techniques.

### Actions

1️⃣ Subquery
Find users who placed orders.

2️⃣ Common Table Expression (CTE)
Calculate total order value before filtering.

3️⃣ Window Function (RANK)
Rank products by price.

Used in analytics dashboards and reporting systems.

---

# 💰 Step 8 — Transactions

## File: `transactions.sql`

Shows how databases prevent data loss.

### Scenario simulated

Customer places an order → payment fails.

Steps:

1. Start transaction
2. Update stock
3. Create order
4. ROLLBACK → undo changes

Second example shows COMMIT → permanent save.

This ensures **data safety in banking and e-commerce systems**.

---

# 🧠 Step 9 — Normalization

## File: `normalization_examples.sql`

Shows why database design matters.

### Before Normalization

Orders table stores:

* user name
* product name
* price

Problem:
Duplicate and inconsistent data.

### After Normalization (3NF)

Data split into:

* users
* products
* orders
* order_items

Benefits:

* No duplication
* Easy updates
* Scalable design

---

# 🔗 Database Relationships

| Relationship        | Type         |
| ------------------- | ------------ |
| User → Orders       | One-to-Many  |
| Order → Order Items | One-to-Many  |
| Products ↔ Orders   | Many-to-Many |

---

# 🎯 Learning Outcomes

After completing this project, the following skills were demonstrated:

* Real database schema design
* Writing 40+ SQL queries
* Using joins and aggregations
* Handling transactions safely
* Applying normalization rules
* Understanding real production SQL workflow

---

⭐ This project represents a complete hands-on SQL learning journey.
