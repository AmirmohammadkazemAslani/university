from pydantic import BaseModel, validator
import json
from fastapi import Form, HTTPException

from database import SessionLocal
import crud
from data.python_data import persian_char, departments, majors


db = SessionLocal()


class Professor(BaseModel):
    LID: int
    Fname: str
    Lname: str
    ID: str
    Department: str
    Major: str
    Birth: str
    BornCity: str
    Address: str
    PostalCode: str
    CPhone: str
    HPhone: str
    Lesson_ids: str
    # LCourseIDs: list[Lesson] = []

    @classmethod
    def as_form(
        cls,
        LID: int = Form(...),
        Fname: str = Form(...),
        Lname: str = Form(...),
        ID: str = Form(...),
        Department: str = Form(...),
        Major: str = Form(...),
        Birth: str = Form(...),
        BornCity: str = Form(...),
        Address: str = Form(max_length=100),
        PostalCode: str = Form(pattern=r"^[0-9]{10}$"),
        CPhone: str = Form(pattern=r"^((\+98|0|098)9\d{9})$"),
        HPhone: str = Form(pattern=r"^0[1|3|4|5|6|7|8|9][0-9]{9}$|^02[0-9]{9}$"),
        Lesson_ids: str = Form(...),
    ):
        return cls(
            LID=LID,
            Fname=Fname,
            Lname=Lname,
            ID=ID,
            Department=Department,
            Major=Major,
            Birth=Birth,
            BornCity=BornCity,
            Address=Address,
            PostalCode=PostalCode,
            CPhone=CPhone,
            HPhone=HPhone,
            Lesson_ids=Lesson_ids,
        )

    @validator("LID")
    def validate_LID(cls, value):
        if len(str(value)) != 6:
            raise HTTPException(status_code=203, detail="LID must be 6 digits.")
        return value

    @validator("Fname")
    def validate_Fname(cls, value):
        if len(value) > 10:
            raise HTTPException(
                status_code=203,
                detail="first name is too long (must be less than 10 characters)",
            )
        for i in value:
            if i not in persian_char:
                raise HTTPException(
                    status_code=203,
                    detail="first name must be only contain persian characters",
                )
        return value

    @validator("Lname")
    def validate_Lname(cls, value):
        if len(value) > 10:
            raise HTTPException(
                status_code=203,
                detail="last name is too long (must be less than 10 characters)",
            )
        for i in value:
            if i not in persian_char:
                raise HTTPException(
                    status_code=203,
                    detail="last name must be only contain persian characters",
                )
        return value

    @validator("ID")
    def validate_meli_code(cls, value):
        value = str(value)
        if value != "updated":
            if not len(value) == 10:
                raise HTTPException(
                    status_code=203, detail="national code is not correct."
                )

            res = 0
            for i, num in enumerate(value[:-1]):
                res = res + (int(num) * (10 - i))

            remain = res % 11
            if remain < 2:
                if not remain == int(value[-1]):
                    raise HTTPException(
                        status_code=203, detail="national code is not correct."
                    )
            else:
                if not (11 - remain) == int(value[-1]):
                    raise HTTPException(
                        status_code=203, detail="national code is not correct."
                    )

            return value
        return value

    @validator("Department")
    def validate_Department(cls, value):
        if value not in departments:
            raise HTTPException(status_code=203, detail="department is not correct.")
        return value

    @validator("Major")
    def validate_Major(cls, value):
        if value not in majors:
            raise HTTPException(status_code=203, detail="major is not correct.")
        return value

    @validator("Birth")
    def validate_Birth(cls, value):
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise HTTPException(status_code=203, detail="date format is not correct.")
        list = value.split("-")
        year = int(list[0])
        if not 1403 > year > 1300:
            raise HTTPException(status_code=203, detail="year is not correct.")
        month = int(list[1])
        if not 1 <= month <= 12:
            raise HTTPException(status_code=203, detail="month is not correct.")
        day = int(list[2])
        if not 1 <= day <= 31:
            raise HTTPException(status_code=203, detail="day is not correct.")
        return value

    @validator("BornCity")
    def validate_BornCity(cls, value):
        with open("project\data\cities.json", "r", encoding="utf-8") as json_file:
            cities = json.load(json_file)
        cities = list(cities)
        new_cities = []
        for c in cities:
            new_cities.append(c["name"])

        if value not in new_cities:
            raise HTTPException(status_code=203, detail="city is not correct.")

        return value

    @validator("Lesson_ids")
    def validate_Lesson_ids(cls, value):
        try:
            lessons = value.split(",")
            for lesson in lessons:
                a = int(lesson)
        except:
            raise HTTPException(status_code=203, detail="Courses id must separate by ,")

        for lesson in lessons:
            lesson = crud.get_lesson(db, int(lesson))
            if lesson is None:
                raise HTTPException(
                    status_code=203, detail="Courses id is not correct!"
                )

        return value
