from fastapi import Depends, HTTPException, Request, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import crud
from schemas import students as schemas
from dependencies import get_db

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = APIRouter()


@router.get("/students/")
def read_students(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    students = crud.get_students(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        request=request, name="student/list.html", context={"students": students}
    )


@router.get("/students/{student_id}/")
def read_student(request: Request, student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse(
        request=request, name="student/page.html", context={"student": db_student}
    )


@router.get("/RegStu")
def create_student(request: Request):
    return templates.TemplateResponse(
        request=request, name="student/add.html", context={}
    )


@router.post("/RegStu")
def create_student_post(
    request: Request,
    student: schemas.Student = Depends(schemas.Student.as_form),
    db: Session = Depends(get_db),
):
    db_student = crud.get_student(db, id=student.STID)
    if db_student:
        raise HTTPException(status_code=400, detail="student already registered")
    crud.create_student(db=db, student=student)
    return RedirectResponse(
        request.url_for("read_students"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/DelStu/{STID}/")
def delete_student(request: Request, STID: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=STID)
    if not db_student:
        raise HTTPException(status_code=400, detail="student not exist")
    crud.delete_student(db=db, id=STID)
    return RedirectResponse(
        request.url_for("read_students"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/UpdateStu/{stid}/")
def update_student(request: Request, stid: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, id=stid)
    if not db_student:
        raise HTTPException(status_code=400, detail="student not exist")
    return templates.TemplateResponse(
        request=request, name="student/update.html", context={"student": db_student}
    )


@router.post("/UpdateStu/{stid}/")
def update_student_post(
    request: Request,
    stid: int,
    student: schemas.Student = Depends(schemas.Student.as_form),
    db: Session = Depends(get_db),
):
    crud.update_student(db=db, id=stid, student=student)
    return RedirectResponse(
        request.url_for("read_students"), status_code=status.HTTP_303_SEE_OTHER
    )
