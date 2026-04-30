from sqlalchemy.orm import Session
from . import models, schemas

def get_users(db: Session, skip: int = 0, limit: int = 10, search: str = None):
    query = db.query(models.User).filter(models.User.is_deleted == False)
    
    if search:
        query = query.filter(models.User.username.contains(search))
        
    return query.offset(skip).limit(limit).all()

def soft_delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.is_deleted = True
        db.commit()
    return user