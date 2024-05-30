import datetime
import sqlite3
from pprint import pprint

db_name = "database_students.db"


def make_read_query(query):
    try:
        with sqlite3.connect(db_name) as conn:
            print(f"База даних {db_name} підключена")
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        data_studs = [{"id": row[0],
                       "name": row[1],
                       "email": row[2],
                       "project": row[3],
                       "score": row[4] if row[4] else 0,
                       } for row in result if result]

        return data_studs

    except sqlite3.Error as e:
        print("Помилка запиту:", e)


def make_write_query(query, *args):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *args)
            conn.commit()
            print(f"Зaпит {query.split()[0]} виконаний з параметрами {args}")

        print("Зєднання з SQLite закрите")
    except sqlite3.Error as e:
        print("Помилка запиту", e)


def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        project TEXT DEFAULT NULL,
        score INTEGER DEFAULT 0,  
        joining_date DATETIME);
    """
    make_write_query(query)


def insert_data(name, email, project=None, score=None):
    joining_date = datetime.datetime.now()
    query = """
    INSERT INTO students (name, email, project, score, joining_date)
               VALUES (?, ?, ?, ?, ?)               
    """

    args = (name, email, project, score, joining_date)
    make_write_query(query, args)


def get_all():
    query = """SELECT * FROM students"""
    return make_read_query(query)


def get_by_id(id):
    query = """SELECT * FROM students WHERE id = ?"""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return {"id": result[0],
                "name": result[1],
                "email": result[2],
                "project": result[3],
                "score": result[4] if result[4] else 0,
                "data": result[5],
                }


def update_data_table(name, email, project=None, score=None):
    join_date = datetime.datetime.now()
    update_query = ("""
        UPDATE students SET name = ?, project = ?, score = ? WHERE email = ?;
        """)

    data_tuple = (name, project, score, email)
    make_write_query(update_query, data_tuple)


def delete_data_table(id):
    query = ("""
        DELETE FROM students WHERE id = ?;
        """)
    make_write_query(query, (id,))


if __name__ == "__main__":
    # sqlite_select_query = "SELECT sqlite_version();"
    # record = make_read_query(sqlite_select_query)
    # print("Версія бази даних SQLite: ", record)

    create_table()

    data_stud = [
        {"name": "Макар Воронкін", "email": "makv@ex.com", "project": "бот_міні_ігри", "score": 100},
        {"name": "Владислав Гудзовський", "email": "vg@ex.com", "project": "бот-гороскоп", "score": 80},
        {"name": "Матвій Байдик", "email": "mb@ex.com", "project": "Birthday_bot", "score": 100},
        {"name": "Богдан Логінський", "email": "bl@ex.com", "project": "погодний бот", "score": 75},
        {"name": "Леонід Поляк", "email": "lp@ex.com", "project": "бот-калькулятор", "score": 75},
        {"name": "Максим Диков", "email": "mad@ex.com", "project": "бот-цитати", "score": 95},
        {"name": "Олександр Борзовець", "email": "ob@ex.com", "project": "бот-перекладач", "score": 90},
        {"name": "Мірослав Колесніков", "email": "mirk@ex.com", "project": "Liverpool F.C.", "score": 90},
        {"name": "Mykhaylo Krytovych korolchuc", "email": "mkk@ex.com", },
    ]

    # for d in data_stud:
    #     insert_data(**d)

    # print(get_by_id(3))

    pprint(get_all())
