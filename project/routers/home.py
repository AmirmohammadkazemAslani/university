from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = APIRouter()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={})
