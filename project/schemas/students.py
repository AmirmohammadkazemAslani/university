from pydantic import BaseModel, validator
import json
from fastapi import Form, HTTPException

from database import SessionLocal
import crud
from models import students as models
from data.python_data import persian_char, departments, majors
from .lessons import Lesson
from .professors import Professor

db = SessionLocal()


class Student(BaseModel):
    STID: int
    Fname: str
    Lname: str
    Father: str
    Birth: str
    IDS: str
    BornCity: str
    Address: str
    PostalCode: str
    CPhone: str
    HPhone: str
    Department: str
    Major: str
    Married: bool
    ID: str
    Courses_ids: str
    Professor_ids: str
    SCourseIDs: list[Lesson] = []
    LIDs: list[Professor] = []

    @classmethod
    def as_form(
        cls,
        STID: int = Form(...),
        Fname: str = Form(...),
        Lname: str = Form(...),
        Father: str = Form(...),
        Birth: str = Form(...),
        IDS: str = Form(...),
        BornCity: str = Form(...),
        Address: str = Form(...),
        PostalCode: str = Form(pattern=r"^[0-9]{10}$"),
        CPhone: str = Form(pattern=r"^((\+98|0|098)9\d{9})$"),
        HPhone: str = Form(pattern=r"^0[1|3|4|5|6|7|8|9][0-9]{9}$|^02[0-9]{9}$"),
        Department: str = Form(...),
        Major: str = Form(...),
        Married: bool = False,
        ID: str = Form(...),
        Courses_ids: str = Form(...),
        Professor_ids: str = Form(...),
    ):
        return cls(
            STID=STID,
            Fname=Fname,
            Lname=Lname,
            Father=Father,
            Birth=Birth,
            IDS=IDS,
            BornCity=BornCity,
            Address=Address,
            PostalCode=PostalCode,
            CPhone=CPhone,
            HPhone=HPhone,
            Department=Department,
            Major=Major,
            Married=Married,
            ID=ID,
            Courses_ids=Courses_ids,
            Professor_ids=Professor_ids,
        )

    @validator("STID")
    def validate_STID(cls, value):
        if len(str(value)) != 11:
            raise HTTPException(
                status_code=203, detail="student code should be 11 digits!"
            )
        year = int(str(value)[:3])
        if not 400 <= year <= 403:
            raise HTTPException(status_code=203, detail="year part is not correct!")
        middle = int(str(value)[3:9])
        if middle != 114150:
            raise HTTPException(status_code=203, detail="middle part is not correct!")
        index = int(str(value)[-2:])
        if not 1 <= index <= 99:
            raise HTTPException(status_code=203, detail="index is not correct!")
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

    @validator("Father")
    def validate_Father(cls, value):
        if len(value) > 10:
            raise HTTPException(
                status_code=203,
                detail="Father name is too long (must be less than 10 characters)",
            )
        for i in value:
            if i not in persian_char:
                raise HTTPException(
                    status_code=203,
                    detail="Father name must be only contain persian characters",
                )
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

    @validator("IDS")
    def validate_IDS(cls, value):
        if len(value) != 10 or value[0] not in persian_char or value[3] != "/":
            raise HTTPException(
                status_code=203, detail="the format of serial is not correct."
            )
        try:
            a = int(value[1:3])
            b = int(value[4:])
        except:
            raise HTTPException(
                status_code=203, detail="the format of serial is not correct."
            )
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

    @validator("ID")
    def validate_meli_code(cls, value):
        value = str(value)
        if value != "updated":
            if (
                db.query(models.Student).filter(models.Student.ID == value).first()
                is not None
            ):
                raise HTTPException(
                    status_code=203,
                    detail="student with this national code alredy exist.",
                )

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

    @validator("Courses_ids")
    def validate_Courses_ids(cls, value):
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

    @validator("Professor_ids")
    def validate_Professor_ids(cls, value):
        try:
            professors = value.split(",")
            for professor in professors:
                a = int(professor)
        except:
            raise HTTPException(
                status_code=203, detail="Professors id must separate by ,"
            )

        for professor in professors:
            professor = crud.get_professor(db, int(professor))
            if professor is None:
                raise HTTPException(
                    status_code=203, detail="Professor id is not correct!"
                )

        return value
