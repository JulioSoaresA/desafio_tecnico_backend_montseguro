from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from redis.asyncio import Redis
from app.cache import get_redis
import json

from .. import models, schemas
from ..db import get_db


router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

CACHE_EXPIRE = 60

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    db_task = models.Task(**task.model_dump())
    if db_task.title == "" or db_task.description == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail="Invalid data")

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Atualizar o cache para que o próximo GET tenha os dados mais recentes
    cache_key = f"task:{db_task.id}"
    await redis.setex(cache_key, CACHE_EXPIRE, json.dumps(db_task.to_dict()))
    
    return db_task.to_dict()


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    db_task = db.query(models.Task).filter_by(id=task_id).first()
    print(db_task)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Non-existent Task")
    
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    
    # Atualizar o cache com os dados atualizados
    cache_key = f"task:{db_task.id}"
    await redis.setex(cache_key, CACHE_EXPIRE, json.dumps(db_task.to_dict()))
    
    return db_task.to_dict()


@router.patch("/{task_id}", response_model=schemas.Task)
async def complete_task(task_id: int, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    task = db.query(models.Task).filter_by(id=task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    
    # Alternar o estado da tarefa
    task.completed = not task.completed
    
    db.commit()
    db.refresh(task)
    
    # Atualizar o cache com os dados atualizados
    cache_key = f"task:{task_id}"
    await redis.setex(cache_key, CACHE_EXPIRE, json.dumps(task.to_dict()))
    
    return task.to_dict()


@router.get("/", response_model=List[schemas.Task])
async def get_tasks(db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    cache_key = "tasks:all"
    
    # Verificar se a lista de tarefas está no cache
    cached_tasks = await redis.get(cache_key)
    if cached_tasks:
        return json.loads(cached_tasks)
    
    tasks = db.query(models.Task).order_by(models.Task.id.asc()).all()
    
    # Armazenar no cache
    tasks_list = [task.to_dict() for task in tasks]
    await redis.setex(cache_key, CACHE_EXPIRE, json.dumps(tasks_list))

    return tasks_list


@router.get("/{task_id}", response_model=schemas.Task)
async def get_task_by_id(task_id: int, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    cache_key = f"task:{task_id}"
    
    # Verificar se a tarefa já está no cache Redis
    cached_task = await redis.get(cache_key)
    if cached_task:
        return json.loads(cached_task)
    
    # Buscar tarefa no banco de dados
    task = db.query(models.Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    
    # Atualizar o cache com os dados da tarefa
    await redis.setex(cache_key, CACHE_EXPIRE, json.dumps(task.to_dict()))
    return task.to_dict()


@router.delete("/{task_id}", response_model=schemas.Task)
async def delete_task(task_id: int, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    db_task = db.query(models.Task).filter_by(id=task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task with id: {task_id} was not found")
    
    db.delete(db_task)
    db.commit()
    
    # Remover o cache da tarefa excluída
    cache_key = f"task:{task_id}"
    await redis.delete(cache_key)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
