from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, schemas, crud_orm, crud_sql

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users/orm")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_orm.get_users(db, skip=skip, limit=limit)

@app.get("/users/raw")
def read_users_raw():
    return crud_sql.get_users_raw()

@app.post("/users/")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    # You can choose to use ORM or Raw here
    db_user = models.User(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user