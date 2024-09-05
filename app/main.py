from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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



@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        **task.model_dump()
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db)):
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


@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    
    if not task.completed:
        task.completed = True
    else: 
        task.completed = False

    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks", response_model=List[schemas.Task])
def get_task(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.asc()).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.Task)
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
