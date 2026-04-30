# 🗄️ Day 6 — Advanced PostgreSQL & FastAPI Integration

This module demonstrates a dual-approach to database management, implementing both Object-Relational Mapping (ORM) and Raw SQL interfaces to handle enterprise-level data operations.

---

## 🚀 Features Implemented

* **Dual-Database Logic**: Seamlessly switch between SQLAlchemy ORM and raw `psycopg2` queries.
* **Connection Resilience**: Implemented connection pooling and context managers for robust error handling and safe resource closure.
* **Security First**: All raw SQL operations utilize parameterized queries to ensure protection against SQL injection.
* **Advanced Data Patterns**: Includes support for soft deletes (using boolean flags), pagination (limit/offset), and keyword searching.
* **Relationship Mapping**: Full implementation of One-to-Many relationships between data entities.
* **Automated Utilities**: Dedicated scripts for schema initialization and database seeding.

---

## 📁 Project Structure & Logic

| File | Functional Responsibility |
| :--- | :--- |
| **`database.py`** | Centralizes connection management. It integrates environment variables for credentials and sets up the SQLAlchemy engine alongside a custom context manager for raw connections. |
| **`models.py`** | Acts as the "source of truth" for the database schema. It defines tables as Python classes and includes advanced features like foreign key constraints and soft-delete logic. |
| **`schemas.py`** | Manages data integrity using Pydantic. These models validate incoming request data and format outgoing API responses. |
| **`crud_orm.py`** | Contains high-level business logic using SQLAlchemy. It handles complex operations like filtered searching and pagination. |
| **`crud_sql.py`** | Demonstrates low-level database interactions. It provides examples of transaction management (Commit/Rollback) using raw SQL strings. |
| **`main.py`** | The application orchestrator. It initializes the FastAPI instance, triggers table creation on startup, and exposes endpoints for both ORM and Raw SQL routes. |
| **`utils/db_init.py`** | A standalone utility script designed to verify connections and generate all database tables automatically. |
| **`utils/seed.py`** | A development tool used to populate the database with initial test records to ensure the system is ready for immediate testing. |

---

## 📸 Documentation & Screenshots

The following images illustrate the API structure and database interactions as seen in the development environment.

### 1. API Endpoint Overview
![API Endpoints](docs/img1.png)

### 2. Database Schema Relationships
![Schema Relationships](docs/img2.png)

### 3. Query Execution & Validation
![Query Validation](docs/img3.png)

---

## 🛠️ Setup and Execution

### 1. Environment Configuration
Create a `.env` file in the root of the **Day-6** directory with your PostgreSQL connection string:
`DATABASE_URL=postgresql://user:password@localhost:5432/dbname`

### 2. Schema Initialization
Run the utility to create your database tables:
`python -m app.utils.db_init`

### 3. Data Seeding
Populate the database with sample development data:
`python -m app.utils.seed`

### 4. Run the Application
Launch the FastAPI server:
`uvicorn app.main:app --reload`