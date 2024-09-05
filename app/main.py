from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    
    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='todo_list', 
                                user='postgres', password='postgres',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


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
def create_task(task: Task, db: Session = Depends(get_db)):
    new_task = models.Task(
        **task.model_dump()
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} does not exist")
    
    task_dict = updated_task.model_dump()
    for key, value in task_dict.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@app.patch("/tasks/{task_id}")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    
    task.completed = True
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks")
def get_task(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} does not exist")
    
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
