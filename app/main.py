from fastapi import FastAPI
from .db import engine
from .routers import task
from .config import settings

app = FastAPI()


app.include_router(task.router)