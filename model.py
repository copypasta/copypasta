import web, datetime
import sqlite3

db = web.database(dbn='sqlite', db='pasta.sqlite')




#db.query("CREATE TABLE entries (id INT AUTO_INCREMENT, title TEXT, content TEXT, posted_on DATETIME, primary key (id));")

def get_posts():
    return db.select('entries', order='id DESC')

def get_id():
    return db.select('entries', order='id DESC')


def get_post(id):
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text):

    result = db.query("select MAX(id) as id from entries")
    newid = int(result[0].id) + 1
    db.insert('entries', id=newid, title=title, content=text, posted_on=datetime.datetime.utcnow())

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('entries', where="id=$id", vars=locals(),
        title=title, content=text)

def transform_datestr(posted_on):
    datetime_obj = datetime.datetime.strptime(posted_on,'%Y-%m-%d %H:%M:%S.%f')
    return web.datestr(datetime_obj)

