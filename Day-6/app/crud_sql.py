from .database import get_raw_conn

def get_users_raw():
    with get_raw_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE is_deleted = FALSE")
            return cur.fetchall()

def create_user_raw(username: str, email: str):
    with get_raw_conn() as conn:
        with conn.cursor() as cur:
            try:
                # Parameterized query to prevent SQL Injection
                cur.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING *",
                    (username, email)
                )
                conn.commit() # Transaction Management
                return cur.fetchone()
            except Exception:
                conn.rollback()
                raise