from fastapi import FastAPI
from .routers import admin, teacher
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(teacher.router)

@app.get("/")
def root():
    return {"message": "School Information Management System"}