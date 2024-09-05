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


def find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(new_task: Task):
    print(new_task)
    return new_task.dict()


@app.get("/tasks")
def get_task():
    return tasks


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int, response: Response):
    task = find_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    return task
