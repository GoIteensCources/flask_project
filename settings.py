import os


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = True
    DB_NAME = f"sqlite:///database.db"
