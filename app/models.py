from typing import List

from db import Base, Session
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    schedule: Mapped[str] = mapped_column()

    students: Mapped[List["Student"]] = relationship(back_populates='group')

    def __str__(self):
        return f"{self.name}"


student_project_assoc_table = sa.Table(
    "student_project_assoc_table",
    Base.metadata,
    sa.Column("student_id", sa.ForeignKey("students.id"), primary_key=True),
    sa.Column("project_id", sa.ForeignKey("projects.id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(25), unique=True)
    age: Mapped[int] = mapped_column(nullable=True)

    group_id = mapped_column(sa.ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates='students')

    projects: Mapped[List["Project"]] = relationship(secondary=student_project_assoc_table)

    def __repr__(self):
        return f"<Student: {self.name}>"

    def __str__(self):
        return f"{self.name}"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(250), default="NOT PROJECT")
    score: Mapped[int] = mapped_column(default=0)

    students: Mapped[List["Student"]] = relationship(secondary=student_project_assoc_table)

    def __str__(self):
        return f"<Project title:{self.title}>"

    def __repr__(self):
        return f"<Project:{self.title}>"
