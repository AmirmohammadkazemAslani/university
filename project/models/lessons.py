from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .middle_tables import student_lesson_association, professor_lesson_association


class Lesson(Base):
    __tablename__ = "lessons"
    CID = Column(Integer, unique=True, primary_key=True)
    CName = Column(String)
    Department = Column(String)
    Credit = Column(Integer)

    student = relationship(
        "Student", secondary=student_lesson_association, back_populates="SCourseIDs"
    )
    professor = relationship(
        "Professor", secondary=professor_lesson_association, back_populates="LCourseIDs"
    )
