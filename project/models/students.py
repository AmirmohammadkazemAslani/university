from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .middle_tables import student_lesson_association, student_professor_association


class Student(Base):
    __tablename__ = "students"

    __table_args__ = {"extend_existing": True}

    STID = Column(Integer, unique=True, primary_key=True)
    Fname = Column(String)
    Lname = Column(String)
    Father = Column(String)
    Birth = Column(String)
    IDS = Column(String)
    BornCity = Column(String)
    Address = Column(String)
    PostalCode = Column(String)
    CPhone = Column(String)
    HPhone = Column(String)
    Department = Column(String)
    Major = Column(String)
    Married = Column(Boolean)
    ID = Column(String, unique=True)
    Courses_ids = Column(String)
    Professor_ids = Column(String)

    SCourseIDs = relationship(
        "Lesson", secondary=student_lesson_association, back_populates="student"
    )
    LIDs = relationship(
        "Professor", secondary=student_professor_association, back_populates="student"
    )

    def get_fullname(self):
        return f"{self.Fname} {self.Lname}"
