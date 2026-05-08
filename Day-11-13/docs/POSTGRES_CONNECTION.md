# PostgreSQL Database Connection - Verified ✅

**Location**: `/docs/POSTGRES_CONNECTION.md`  
**Status**: ✅ Complete & Verified  
**Last Updated**: May 8, 2026

---

## Connection Status: SUCCESS

The application has been successfully connected to the PostgreSQL database `fastapi_demo`.

### Connection Details
- **Host**: localhost
- **Port**: 5432
- **Database**: fastapi_demo
- **Username**: postgres
- **URL Format**: `postgresql://postgres:anand%4012@localhost/fastapi_demo`

> **Note**: The password contains special character `@` which is URL-encoded as `%40` in the connection string.

---

## Database Schema Verification

### Tables Created (8 total)
✅ users
✅ categories
✅ products
✅ carts
✅ cart_items
✅ orders
✅ order_items
✅ reviews

### Table Details

#### users
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| username | VARCHAR(50) | UNIQUE, NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password | VARCHAR(255) | NOT NULL |
| role | VARCHAR(20) | DEFAULT 'user' |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |

#### categories
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| name | VARCHAR(100) | UNIQUE, NOT NULL |
| description | TEXT | Optional |

#### products
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| description | TEXT | Optional |
| price | NUMERIC(10, 2) | NOT NULL |
| stock | INTEGER | Default 0 |
| category_id | INTEGER | FOREIGN KEY → categories |
| **image_url** | VARCHAR(500) | **ADDED** (not in original schema) |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |

#### carts
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | UNIQUE, FOREIGN KEY → users |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |

#### cart_items
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| cart_id | INTEGER | FOREIGN KEY → carts |
| product_id | INTEGER | FOREIGN KEY → products |
| quantity | INTEGER | Default 1 |
| UNIQUE(cart_id, product_id) | | Constraint |

#### orders
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users |
| total | NUMERIC(10, 2) | NOT NULL |
| status | VARCHAR(50) | DEFAULT 'pending' |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |

#### order_items
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| order_id | INTEGER | FOREIGN KEY → orders |
| product_id | INTEGER | FOREIGN KEY → products |
| quantity | INTEGER | NOT NULL |
| price | NUMERIC(10, 2) | NOT NULL |

#### reviews
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | PRIMARY KEY |
| user_id | INTEGER | FOREIGN KEY → users |
| product_id | INTEGER | FOREIGN KEY → products |
| rating | INTEGER | CHECK (1-5) |
| comment | TEXT | Optional |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |
| UNIQUE(user_id, product_id) | | Constraint |

---

## Test Data Seeded

### Users
- **Admin User**: admin@ecommerce.com / Admin123 (role: admin)
- **Customer User**: customer@ecommerce.com / Customer123 (role: customer)

### Categories
1. Electronics
2. Clothing
3. Books

### Products (7 total)
1. **Laptop** - Electronics - $1,299.99
2. **Smartphone** - Electronics - $899.99
3. **Headphones** - Electronics - $199.99
4. **T-Shirt** - Clothing - $29.99
5. **Jeans** - Clothing - $59.99
6. **Python Programming** - Books - $39.99
7. **FastAPI Guide** - Books - $49.99

---

## Configuration

### Environment Variables (.env)
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fastapi_demo
SECRET_KEY=dev-secret-key-not-for-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Requirements Updates
PostgreSQL driver for Python:
```
psycopg2-binary==2.9.12
```

---

## How to Setup PostgreSQL Connection

### Step 1: Install PostgreSQL
If not already installed:
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql postgresql-contrib`

### Step 2: Start PostgreSQL Service
```bash
# Windows
net start PostgreSQL14  # or your version

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Step 3: Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE fastapi_demo;

# List databases to verify
\l

# Exit psql
\q
```

### Step 4: Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fastapi_demo
```

### Step 5: Verify Connection
```bash
# Test database connection
python tests/test_db_connection.py
```

---

## How to Test the Connection

### 1. Run Connection Test Script
```bash
python tests/test_db_connection.py
```

**Expected Output**:
```
✅ Connection successful!
✅ All 8 tables exist
✅ Database seeded with test data
```

### 2. Seed Database (if needed)
```bash
python -m app.utils.seed

# Or using direct script
python seed_postgres.py
```

### 3. Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 4. Access Swagger UI
Navigate to: `http://localhost:8000/docs`

### 5. Test API Endpoints
**Register a new user**:
```
POST /auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "username": "testuser",
  "password": "Test@123"
}
```

**Login**:
```
POST /auth/login
Content-Type: application/json

{
  "email": "admin@ecommerce.com",
  "password": "Admin123"
}
```

**Get Products**:
```
GET /products
```

**Search Products**:
```
GET /products?search=laptop
```

**Filter by Category**:
```
GET /products?category_id=1
```

---

## Files Created/Modified

### New Files
- `test_db_connection.py` → Moved to `/tests/test_db_connection.py`
- `seed_postgres.py` - PostgreSQL seed data script

### Modified Files
- `.env` - Updated DATABASE_URL for PostgreSQL
- `requirements.txt` - Added psycopg2-binary
- `schema.sql` - Products table manually altered to add image_url column

---

## Troubleshooting

### Connection Failed: Password Authentication Failed
**Problem**: `FATAL: password authentication failed for user 'postgres'`

**Solutions**:
1. Verify PostgreSQL is running
2. Check that the password is correct
3. Ensure special characters are URL-encoded (@ = %40)
4. Test connection directly:
   ```bash
   psql -U postgres -h localhost
   ```

### Connection Failed: Database Does Not Exist
**Problem**: `FATAL: database "fastapi_demo" does not exist`

**Solution**:
```bash
psql -U postgres

# Create the database
CREATE DATABASE fastapi_demo;

# Exit
\q
```

### Connection Timeout
**Problem**: Connection attempt times out

**Solutions**:
1. Ensure PostgreSQL is running:
   ```bash
   pg_isready -h localhost -p 5432
   ```
2. Check firewall allows port 5432
3. Verify PostgreSQL is listening on localhost:
   ```bash
   psql -U postgres -h localhost
   ```

### Tables Not Created
**Problem**: Database exists but tables are empty

**Solution**:
```bash
# Run the seed script
python -m app.utils.seed

# Or use direct seed
python seed_postgres.py

# Verify tables
python tests/test_db_connection.py
```

### Special Character Password Issues
**Problem**: Password with special characters causes connection error

**Solution**:
URL-encode special characters:
```python
from urllib.parse import quote_plus

password = "anand@12"
encoded = quote_plus(password)  # Results in: anand%4012

# Use in DATABASE_URL:
# postgresql://postgres:anand%4012@localhost/fastapi_demo
```

Common URL encodings:
| Character | Encoded |
|-----------|---------|
| @ | %40 |
| # | %23 |
| $ | %24 |
| % | %25 |
| & | %26 |
| : | %3A |
| / | %2F |
| ? | %3F |
| = | %3D |

---

## Connection Best Practices

### 1. Credentials Management
- ✅ Use `.env` file for local credentials
- ✅ Never commit `.env` with real passwords
- ✅ Use `.env.example` as template
- ❌ Never hardcode credentials in code

### 2. Environment Variables
```env
# Development
DATABASE_URL=postgresql://postgres:dev_password@localhost:5432/fastapi_demo
DEBUG=true

# Production (use system environment variables)
export DATABASE_URL="postgresql://prod_user:secure_pwd@prod-host/ecommerce"
export DEBUG=false
```

### 3. Connection String Format
```
postgresql://[user[:password]@][host][:port]/[database]
```

Example with all parts:
```
postgresql://postgres:your_password@localhost:5432/fastapi_demo
```

### 4. Connection Pooling (for production)
For production deployments, consider using PgBouncer for connection pooling.

### 5. SSL Connections (for production)
For remote PostgreSQL servers:
```
postgresql://user:password@host:5432/database?sslmode=require
```

---

## Common Commands

### Using psql (PostgreSQL CLI)

```bash
# Connect to PostgreSQL
psql -U postgres

# Connect to specific database
psql -U postgres -d fastapi_demo

# List databases
\l

# List tables in current database
\dt

# Describe a specific table
\d products

# Run SQL file
\i schema.sql

# Get help
\h SELECT

# Exit
\q
```

### Backup and Restore

```bash
# Backup database
pg_dump -U postgres fastapi_demo > backup.sql

# Restore database
psql -U postgres fastapi_demo < backup.sql

# Backup specific table
pg_dump -U postgres -t products fastapi_demo > products_backup.sql
```

---

## Performance Monitoring

### Check Active Connections
```sql
SELECT datname, pid, usename, state FROM pg_stat_activity;
```

### View Database Size
```sql
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) 
FROM pg_database 
ORDER BY pg_database_size DESC;
```

### View Table Sizes
```sql
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size DESC;
```

---

## Next Steps

1. ✅ PostgreSQL connection verified
2. ✅ Database schema created and validated
3. ✅ Test data seeded
4. Start FastAPI server and test endpoints
5. Deploy to production with PostgreSQL
6. Set up automated backups
7. Monitor connection and performance

---

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL Guide](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/advanced/sql-databases/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

**Status**: ✅ Connection Verified  
**Last Tested**: May 8, 2026  
**Database**: fastapi_demo  
**All systems operational! 🚀**
