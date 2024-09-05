from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    
    
tasks = [
        {"id": 1, "title": "task 01", "description": "descricao 01", "completed": False}, 
        {"id": 2, "title": "task 02", "description": "descricao 02", "completed": False}
    ]


# Função para buscar uma task pelo id
def find_task(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)


# Função para buscar o índice de uma task pelo id
def find_index_task(task_id):
    return next((i for i, task in enumerate(tasks) if task["id"] == task_id), None)



@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(new_task: Task):
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    task_dict = new_task.model_dump()
    task_dict["id"] = new_id
    tasks.append(task_dict)
    return task_dict


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


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    index = find_index_task(task_id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} does not exist")
    tasks.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
