from fastapi import FastAPI
from .routers import admin, auth, teacher, student, course
from .database import engine
from .models import adminModel, teacherModel, studentModel, courseModel

adminModel.Base.metadata.create_all(bind=engine)
teacherModel.Base.metadata.create_all(bind=engine)
studentModel.Base.metadata.create_all(bind=engine)
courseModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(teacher.router)
app.include_router(student.router)
app.include_router(course.router)

@app.get("/")
def root():
    return {"message": "School Information Management System"}