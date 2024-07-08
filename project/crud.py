from sqlalchemy.orm import Session
from models import students as student_models
from models import lessons as lesson_models
from models import professors as professor_models

from schemas import students as student_schemas
from schemas import lessons as lesson_schemas
from schemas import professors as professor_schemas



def set_lesson(db, table, lessons):
    for lesson in lessons:
        lesson = get_lesson(db, int(lesson))
        table.SCourseIDs.append(lesson)

def set_professor(db, table, professors):
    for professor in professors:
        professor = get_professor(db, int(professor))
        table.LIDs.append(professor)

def set_professor_lesson(db, table, lessons):
    for lesson in lessons:
        lesson = get_lesson(db, int(lesson))
        table.LCourseIDs.append(lesson)



# student

def get_student(db: Session, id: int):
    return db.query(student_models.Student).filter(student_models.Student.STID == id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(student_models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: student_schemas.Student):
    db_student = student_models.Student(STID=student.STID, Fname=student.Fname, Lname=student.Lname, Father=student.Father, Birth=student.Birth, IDS=student.IDS, BornCity=student.BornCity, Address=student.Address, PostalCode=student.PostalCode, CPhone=student.CPhone, HPhone=student.HPhone, Department=student.Department,  Major=student.Major,  Married=student.Married, ID=student.ID, Courses_ids=student.Courses_ids, Professor_ids=student.Professor_ids)

    set_lesson(db, db_student, student.Courses_ids.split(","))
    set_professor(db, db_student, student.Professor_ids.split(","))

    db.add(db_student)
    db.commit()
    db.refresh(db_student)


def delete_student(db: Session, id: int):
    db_student = db.query(student_models.Student).filter(student_models.Student.STID == id).first()
    db.delete(db_student)
    db.commit()


def update_student(db: Session, id: int, student: student_schemas.Student):
    db_student = db.query(student_models.Student).filter(student_models.Student.STID == id).first()
    db_student.Fname = student.Fname
    db_student.Lname = student.Lname
    db_student.Father = student.Father
    db_student.Birth = student.Birth
    db_student.IDS = student.IDS
    db_student.BornCity = student.BornCity
    db_student.Address = student.Address
    db_student.PostalCode = student.PostalCode
    db_student.CPhone = student.CPhone
    db_student.HPhone = student.HPhone
    db_student.Department = student.Department
    db_student.Major = student.Major
    db_student.Married = student.Married
    db_student.Courses_ids = student.Courses_ids
    db_student.Professor_ids = student.Professor_ids

    db_student.SCourseIDs = []
    db_student.LIDs = []
    set_lesson(db, db_student, student.Courses_ids.split(","))
    set_professor(db, db_student, student.Professor_ids.split(","))

    db.commit()



# professor

def get_professor(db: Session, id: int):
    return db.query(professor_models.Professor).filter(professor_models.Professor.LID == id).first()

def get_professors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(professor_models.Professor).offset(skip).limit(limit).all()

def create_professor(db: Session, professor: professor_schemas.Professor):
    db_professor = professor_models.Professor(LID=professor.LID, Fname=professor.Fname, Lname=professor.Lname, ID=professor.ID, Department=professor.Department, Major=professor.Major, Birth=professor.Birth, BornCity=professor.BornCity, Address=professor.Address, PostalCode=professor.PostalCode, CPhone=professor.CPhone, HPhone=professor.HPhone, Lesson_ids=professor.Lesson_ids)

    set_professor_lesson(db, db_professor, professor.Lesson_ids.split(","))

    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)

def delete_professor(db: Session, id: int):
    db_professor = db.query(professor_models.Professor).filter(professor_models.Professor.LID == id).first()
    db.delete(db_professor)
    db.commit()

def update_professor(db: Session, id: int, professor: professor_schemas.Professor):
    db_professor = db.query(professor_models.Professor).filter(professor_models.Professor.LID == id).first()
    db_professor.Fname = professor.Fname
    db_professor.Lname = professor.Lname
    db_professor.Department = professor.Department
    db_professor.Major = professor.Major
    db_professor.Birth = professor.Birth
    db_professor.BornCity = professor.BornCity
    db_professor.Address = professor.Address
    db_professor.PostalCode = professor.PostalCode
    db_professor.CPhone = professor.CPhone
    db_professor.HPhone = professor.HPhone
    db_professor.Lesson_ids = professor.Lesson_ids

    db_professor.LCourseIDs = []
    set_professor_lesson(db, db_professor, professor.Lesson_ids.split(","))

    db.commit()



# lesson

def get_lesson(db: Session, id: int):
    return db.query(lesson_models.Lesson).filter(lesson_models.Lesson.CID == id).first()

def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(lesson_models.Lesson).offset(skip).limit(limit).all()

def create_lesson(db: Session, lesson: lesson_schemas.Lesson):
    db_lesson = lesson_models.Lesson(CID=lesson.CID, CName=lesson.CName, Department=lesson.Department, Credit=lesson.Credit)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)

def delete_lesson(db: Session, id: int):
    db_lesson = db.query(lesson_models.Lesson).filter(lesson_models.Lesson.CID == id).first()
    db.delete(db_lesson)
    db.commit()

def update_lesson(db: Session, id: int, lesson: lesson_schemas.Lesson):
    db_lesson = db.query(lesson_models.Lesson).filter(lesson_models.Lesson.CID == id).first()
    db_lesson.CName = lesson.CName
    db_lesson.Department = lesson.Department
    db_lesson.Credit = lesson.Credit
    db.commit()


