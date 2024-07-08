from pydantic import BaseModel, validator
from fastapi import Form, HTTPException

from database import SessionLocal
from data.python_data import persian_char, departments, majors

db = SessionLocal()


class Lesson(BaseModel):
    CID: int
    CName: str
    Department: str
    Credit: int

    @classmethod
    def as_form(
        cls,
        CID: int = Form(...),
        CName: str = Form(...),
        Department: str = Form(...),
        Credit: int = Form(ge=1, le=4),
    ):
        return cls(CID=CID, CName=CName, Department=Department, Credit=Credit)

    @validator("CID")
    def validate_CID(cls, value):
        if len(str(value)) != 5:
            raise HTTPException(status_code=203, detail="CID must be 5 digits.")
        return value

    @validator("CName")
    def validate_CName(cls, value):
        if len(value) > 25:
            raise HTTPException(
                status_code=203,
                detail="Cname is too long (must be less than 25 characters)",
            )
        for i in value:
            if i not in persian_char:
                raise HTTPException(
                    status_code=203,
                    detail="Cname must be only contain persian characters",
                )
        return value

    @validator("Department")
    def validate_Department(cls, value):
        if value not in departments:
            raise HTTPException(status_code=203, detail="department is not correct.")
        return value
