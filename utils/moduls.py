from database.db_conf import database

db = database('users')
def add_deeplink(user_id):
    fixture = 'https://t.me/chtopofacebot?start='
    result = fixture + str(user_id)
    db.add_deeplink(user_id=user_id, deeplink=result)
