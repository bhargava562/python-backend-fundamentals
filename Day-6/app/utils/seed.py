from app.database import SessionLocal, engine
from app import models

def seed_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if data exists
    if db.query(models.User).count() == 0:
        test_user = models.User(username="dev_user", email="dev@example.com")
        db.add(test_user)
        db.commit()
        print("Database Seeded!")
    db.close()

if __name__ == "__main__":
    seed_db()