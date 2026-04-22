from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EchoRequest(BaseModel):
    message: str
    times: int

class UserCreate(BaseModel):
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(data: EchoRequest):
    return {
        "result": data.message * data.times
    }

@app.post("/users")
def create_user(data: UserCreate):
    return {
        "id": 1,
        "name": data.name
    }