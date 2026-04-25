from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = []
next_id = 1

class EchoRequest(BaseModel):
    message: str
    times: int

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(data: EchoRequest):
    return {
        "result": data.message * data.times
    }

@app.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    global next_id
    user = {
        "id": next_id,
        "name": data.name
    }
    users.append(user)
    next_id += 1

    return user

# list[UserResponse] means "the response will be a list
# of users, where each user matches UserResponse"
@app.get("/users", response_model=list[UserResponse])
def get_users():
    return users

@app.get("/users/{id}", response_model=UserResponse)
def get_user_id(id: int):
    for user in users:
        if user["id"] == id:
            return user
    raise HTTPException(status_code=404, detail="User Not Found")

@app.delete("/users/{id}")
def delete_user_id(id: int):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return {"message": f"Successfully removed user {id}"}
    raise HTTPException(status_code=404, detail="User Not Found")
