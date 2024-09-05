from fastapi import FastAPI
from .db import engine
from .routers import task

app = FastAPI()


app.include_router(task.router)