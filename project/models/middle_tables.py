from sqlalchemy import Table, ForeignKey, Integer, Column
from database import Base


student_lesson_association = Table(
    "student_lesson",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.STID")),
    Column("lesson_id", Integer, ForeignKey("lessons.CID")),
    extend_existing=True,
)

student_professor_association = Table(
    "student_professor",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.STID")),
    Column("professor_id", Integer, ForeignKey("professors.LID")),
    extend_existing=True,
)

professor_lesson_association = Table(
    "professor_lesson",
    Base.metadata,
    Column("professor_id", Integer, ForeignKey("professors.LID")),
    Column("lesson_id", Integer, ForeignKey("lessons.CID")),
    extend_existing=True,
)
