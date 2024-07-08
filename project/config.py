from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

# from . import models
from database import engine, Base
from routers import students, lessons, professors, home


# models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(students.router, tags=["students"])
app.include_router(lessons.router, tags=["lessons"])
app.include_router(professors.router, tags=["professors"])
app.include_router(home.router, tags=["home"])

app.mount("/static", StaticFiles(directory="static"), name="static")
