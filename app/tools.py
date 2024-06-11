from datetime import datetime


def get_age(birth_day):
    date_birth = datetime.strptime(birth_day, "%Y-%m-%d")
    date_now = datetime.now()
    age = date_now.year - date_birth.year - ((date_birth.month, date_birth.day) > (date_now.month, date_now.day))

    return age
