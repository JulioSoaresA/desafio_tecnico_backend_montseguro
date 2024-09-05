from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db import get_db


router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        **task.model_dump()
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/{task_id}", response_model=schemas.Task)
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


@router.patch("/{task_id}", response_model=schemas.Task)
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


@router.get("/", response_model=List[schemas.Task])
def get_task(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.asc()).all()
    return tasks


@router.get("/{task_id}", response_model=schemas.Task)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id).first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} does not exist")
    
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
