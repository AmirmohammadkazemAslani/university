from fastapi import Depends, HTTPException, Request, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import crud
from schemas import professors as schemas
from dependencies import get_db

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = APIRouter()


@router.get("/professors/")
def read_professors(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    professors = crud.get_professors(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        request=request, name="professor/list.html", context={"professors": professors}
    )


@router.get("/professors/{professo_id}/")
def read_professor(request: Request, professo_id: int, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=professo_id)
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return templates.TemplateResponse(
        request=request, name="professor/page.html", context={"professor": db_professor}
    )


@router.get("/RegPro/")
def create_professor(request: Request):
    return templates.TemplateResponse(
        request=request, name="professor/add.html", context={}
    )


@router.post("/RegPro/")
def create_professor_post(
    request: Request,
    professor: schemas.Professor = Depends(schemas.Professor.as_form),
    db: Session = Depends(get_db),
):
    db_professor = crud.get_professor(db, id=professor.LID)
    if db_professor:
        raise HTTPException(status_code=400, detail="Professor already registered")
    crud.create_professor(db=db, professor=professor)
    return RedirectResponse(
        request.url_for("read_professors"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/DelPro/{LID}/")
def delete_professor(request: Request, LID: int, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=LID)
    if not db_professor:
        raise HTTPException(status_code=400, detail="Professor not exist")
    crud.delete_professor(db=db, id=LID)
    return RedirectResponse(
        request.url_for("read_professors"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/UpdatePro/{lid}/")
def update_professor(request: Request, lid: int, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, id=lid)
    if not db_professor:
        raise HTTPException(status_code=400, detail="Professor not exist")
    return templates.TemplateResponse(
        request=request,
        name="professor/update.html",
        context={"professor": db_professor},
    )


@router.post("/UpdatePro/{lid}/")
def update_professor_post(
    request: Request,
    lid: int,
    professor: schemas.Professor = Depends(schemas.Professor.as_form),
    db: Session = Depends(get_db),
):
    crud.update_professor(db=db, id=lid, professor=professor)
    return RedirectResponse(
        request.url_for("read_professors"), status_code=status.HTTP_303_SEE_OTHER
    )
