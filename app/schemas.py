from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str
    description: str


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    
    class Config:
        orm_mode = True
