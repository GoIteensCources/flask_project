from flask import url_for, request
from flask import render_template, redirect, abort

from app.models import Group, Student, Project
from app.tools import get_age
from sqlalchemy import text, select, update
# from data import *
from data.data_db import create_table, insert_data, get_all, get_by_id, delete_data_table

from app import app
from db import Session


@app.route('/')
def home():
    with Session() as session:
        query = text("SELECT * FROM groups")
        group = session.execute(query).one()
    return render_template("base.html",
                           title="FlaskCources",
                           group=group.name
                           )


@app.route('/our_students')
def students(message_info=None):
    with Session() as session:
        stmt = select(Group).where(Group.id == 1)
        group = session.scalar(stmt)

        students = session.scalars(select(Student)).all()

    context = {
        "title": "Students",
        "students": students,
        "group": group,
        "message": message_info
    }
    return render_template("students/students_page.html", **context)


@app.route('/add_student', methods=["GET", "POST"])
def add_student():
    with Session() as session:
        group = session.scalar(select(Group))

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


@app.route('/student/<int:_id>')
def details_student(_id):
    with Session() as session:
        group = session.scalar(select(Group))

        stmt = select(Student).where(Student.id == _id)
        student = session.scalars(stmt).one()
        print(student)

        context = {
            "group": group.name,
            "student": student,
            "projects": student.projects,
            "title": f"Student {student.name}",
        }
    return render_template("students/detail_student.html", **context)


@app.route('/drop_student/<int:id_>')
def delete_student(id_):
    with Session() as session:
        student = session.get(Student, id_)
        proj_st = student.projects
        for p in proj_st:
            if len(p.students) == 1:
                session.delete(p)
                session.flush()

        session.delete(student)
        session.commit()

    return redirect(url_for("students", message_info=f"Запис #{id_} видалено"))


@app.route('/update_student/<int:id_>', methods=['GET', 'POST'])
def update_student(id_):
    with Session() as session:
        group = session.query(Group).one()

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']

            stmt = update(Student).where(Student.id == id_).values(name=name, age=age, email=email)
            session.execute(stmt)
            session.flush()
            session.commit()

            return redirect(url_for("students"))
        else:
            student = session.get(Student, id_)

            context = {
                "student": student,
                "title": "Update student",
                "group": group
            }
            return render_template('students/form_add_student.html', **context)


# Проекти

@app.route('/projects')
def projects():
    with Session() as session:
        group = session.scalar(select(Group))

        all_projects = session.scalars(select(Project)).all()

        proj_students = []
        for proj in all_projects:
            proj_students.append(proj.students)

        result_proj = list(zip(all_projects, proj_students))

        context = {
            "group": group.name,
            "title": f"All projects",
            "projects": result_proj
        }

    return render_template("projects/all_projects.html", **context)


@app.route('/add_projects', methods=["POST", "GET"])
def add_project():
    with Session() as session:
        group = session.scalar(select(Group))

        if request.method == "POST":
            title = request.form.get("title")
            score = request.form.get("score")
            students = request.form.getlist("students")

            item_students = session.query(Student).where(Student.id.in_(students)).all()
            item = Project(title=title, score=score, students=item_students)

            session.add(item)
            session.commit()

            return redirect(url_for("projects"))

        else:
            students = session.scalars(select(Student)).all()

            context = {
                "group": group.name,
                "title": f"All projects",
                "students": students
            }
            return render_template("projects/add_project.html", **context)


@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html")
