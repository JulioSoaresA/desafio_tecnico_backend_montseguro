from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    
    
tasks = [
        {"id": 1, "title": "task 01", "description": "descricao 01"}, 
        {"id": 2, "title": "task 02", "description": "descricao 02"}
    ]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(new_task: Task):
    print(new_task)
    return new_task.dict()
