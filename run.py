from pprint import pprint
from app import app
from db import create_db, drop_db
from app.models import *


if __name__ == "__main__":
    print(app.url_map)
    create_db()
    app.run()
