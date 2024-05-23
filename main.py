from flask import Flask, url_for
from flask import render_template, redirect, abort
from data import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("base.html",
                           title="FlaskCources",
                           group=group
                           )


@app.route('/our_students')
def students():
    context = {
        "title": "StudentsProj",
        "students": studenets,
        "max_score": max_score,
        "group": group
    }
    return render_template("students_page.html", **context)


@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html")


if __name__ == "__main__":
    print(app.url_map)
    app.run(host='localhost', port=5050, debug=True)
