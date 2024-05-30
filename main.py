from pprint import pprint

from flask import Flask, url_for, request
from flask import render_template, redirect, abort
from data import *
from data.data_db import create_table, insert_data, get_all, get_by_id, delete_data_table

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("base.html",
                           title="FlaskCources",
                           group=group
                           )


@app.route('/our_students')
def students(message_info=None):
    studenets = get_all()
    context = {
        "title": "StudentsProj",
        "students": studenets,
        "max_score": max_score,
        "group": group,
        "message":message_info
    }

    pprint(studenets)

    return render_template("students_page.html", **context)


@app.route('/add_student', methods=["get", "post"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        project = request.form["project"]
        score = request.form["score"]

        insert_data(name, email, project, score)

        return redirect(url_for("students"))
    else:
        return render_template("form_add_student.html", title="add student", group=group)


@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html")


@app.route('/student/<int:id_>')
def details_student(id_):

    student = get_by_id(id_)
    print(student)

    context = {
        "title": f"{student}",
        "group": group,
        "student": student,
    }
    return render_template("detail_student.html", **context)


@app.route('/d_student/<int:id_>')
def delete_student(id_):
    delete_data_table(id_)
    return redirect(url_for("students", message_info=f"Запис #{id_} видалено"))


if __name__ == "__main__":
    print(app.url_map)
    create_table()
    app.run(host='localhost', port=5050, debug=True)
