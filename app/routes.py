from datetime import datetime
from pprint import pprint

from flask import url_for, request
from flask import render_template, redirect, abort

from app.models import Group, Student
from app.tools import get_age
from data import *
from data.data_db import create_table, insert_data, get_all, get_by_id, delete_data_table


from app import app
from db import Session

@app.route('/')
def home():
    with Session() as session:
        group = session.query(Group).first()
    return render_template("base.html",
                           title="FlaskCources",
                           group=group.name
                           )


@app.route('/our_students')
def students(message_info=None):
    with Session() as session:
        studenets = session.query(Student).all()
        group = session.query(Group).first()

    context = {
        "title": "Students",
        "students": studenets,
        "group": group,
        "message": message_info
    }
    return render_template("students/students_page.html", **context)


@app.route('/add_student', methods=["GET", "POST"])
def add_student():
    with Session() as session:
        group = session.query(Group).first()

        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            birth_day = request.form["birth_day"]

            item = Student(name=name,
                           email=email,
                           age=get_age(birth_day),
                           group_id=group.id)

            session.add(item)
            session.commit()

            return redirect(url_for("students"))
        else:
            return render_template("students/form_add_student.html", title="add student", group=group)


@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html")


@app.route('/student/<int:_id>')
def data_student(_id):
    with Session() as session:
        group = session.query(Group).first()
        student = session.query(Student).where(Student.id == _id).first()
        print(student)

        breakpoint()

        context = {
            "group": group.name,
            "student": student,
            "projects": student.projects,
            "title": f"Student {student.name}",
        }
    return render_template("student/details_student.html", **context)

@app.route('/d_student/<int:id_>')
def delete_student(id_):
    delete_data_table(id_)
    return redirect(url_for("students", message_info=f"Запис #{id_} видалено"))

