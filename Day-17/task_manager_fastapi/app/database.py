from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Using in-memory SQLite database for fast, temporary storage
# StaticPool ensures all connections use the same in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use StaticPool to keep single connection
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get DB session (Interview: This is Dependency Injection!)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database on import
def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)