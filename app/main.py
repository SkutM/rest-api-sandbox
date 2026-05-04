from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.database import Base, engine, get_db
from app.models import User
from app.schemas import EchoRequest, UserCreate, UserResponse, UserUpdate
from app.crud import get_user_by_id, get_all_users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(data: EchoRequest):
    return {
        "result": data.message * data.times
    }

@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = User(name=data.name)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# list[UserResponse] means "the response will be a list
# of users, where each user matches UserResponse"
@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return get_all_users(db, limit=limit, offset=offset)

@app.get("/users/{id}", response_model=UserResponse)
def get_user_id(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    return user

@app.delete("/users/{id}", status_code=204)
def delete_user_id(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)

    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    db.delete(user)
    db.commit()
    # db.refresh(user) will fail

@app.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)

    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)

    return user