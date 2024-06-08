import datetime

from database.db_conf import database


def get_succes(user_id: int, db: database) -> bool:
    date = db.get_data(user_id)
    if date:
        date = date.split('-')
        last_date = datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        sept = str(last_date - datetime.date.today()).split(' ')
        if len(sept) != 1:
            return True
        return False
    return True

# print(type('{"code":100000,"result":{"job_id":"f7c330cd-92e1-4f4b-8c4c-47648c88106b"},"message":{"en":"Request Success."}}'))
