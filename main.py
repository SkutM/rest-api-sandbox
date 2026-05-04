from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

engine = create_engine("sqlite:///./test.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# users = []
# next_id = 1

class EchoRequest(BaseModel):
    message: str
    times: int

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

class UserUpdate(BaseModel):
    name: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(data: EchoRequest):
    return {
        "result": data.message * data.times
    }

def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def get_all_users(db: Session):
    return db.query(User).all()

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
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)

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