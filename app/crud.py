from sqlalchemy.orm import Session
from app.models import User

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session, limit: int = 10, offset: int = 0):
    return db.query(User).offset(offset).limit(limit).all()