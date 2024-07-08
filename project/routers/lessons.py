from fastapi import Depends, HTTPException, Request, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import crud
from schemas import lessons as schemas
from dependencies import get_db

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = APIRouter()


@router.get("/lessons/")
def read_lessons(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    lessons = crud.get_lessons(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        request=request, name="lesson/list.html", context={"lessons": lessons}
    )


@router.get("/lessons/{lesson_id}/")
def read_lesson(request: Request, lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return templates.TemplateResponse(
        request=request, name="lesson/page.html", context={"lesson": db_lesson}
    )


@router.get("/RegLesson/")
def create_lesson(request: Request):
    return templates.TemplateResponse(
        request=request, name="lesson/add.html", context={}
    )


@router.post("/RegLesson/")
def create_lesson_post(
    request: Request,
    lesson: schemas.Lesson = Depends(schemas.Lesson.as_form),
    db: Session = Depends(get_db),
):
    db_lesson = crud.get_lesson(db, id=lesson.CID)
    if db_lesson:
        raise HTTPException(status_code=400, detail="Lesson already registered")
    crud.create_lesson(db=db, lesson=lesson)
    return RedirectResponse(
        request.url_for("read_lessons"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/DelLesson/{CID}/")
def delete_lesson(request: Request, CID: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=CID)
    if not db_lesson:
        raise HTTPException(status_code=400, detail="Lesson not exist")
    crud.delete_lesson(db=db, id=CID)
    return RedirectResponse(
        request.url_for("read_lessons"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/UpdateLesson/{cid}/")
def update_lesson(request: Request, cid: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson(db, id=cid)
    if not db_lesson:
        raise HTTPException(status_code=400, detail="lesson not exist")
    return templates.TemplateResponse(
        request=request, name="lesson/update.html", context={"lesson": db_lesson}
    )


@router.post("/UpdateLesson/{cid}/")
def update_lesson_post(
    request: Request,
    cid: int,
    lesson: schemas.Lesson = Depends(schemas.Lesson.as_form),
    db: Session = Depends(get_db),
):
    crud.update_lesson(db=db, id=cid, lesson=lesson)
    return RedirectResponse(
        request.url_for("read_lessons"), status_code=status.HTTP_303_SEE_OTHER
    )
