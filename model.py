""" model module for copypasta online clipboard """
""" AppSec Fall 2012 """
""" George Ryabov, Kelvin Yang, David Chan """
""" requires webpy 0.3 """

import web, datetime
import sqlite3

db = web.database(dbn='sqlite', db='pasta.sqlite')
userdb = web.database(dbn='sqlite', db='users.sqlite')



#db.query("CREATE TABLE entries (id INT AUTO_INCREMENT, title TEXT, content TEXT, posted_on DATETIME, primary key (id));")

def get_posts(user):
    return db.select('entries', order='id DESC', where='owner=$user', vars=locals())

def set_owner(sessionid, user):
    db.update('entries', where="owner=$sessionid", vars=locals(),
        owner=user)

def get_id(user):
    return db.select('entries', order='id DESC', where='owner=$user', vars=locals())


def get_post(id, user):
    try:
        return db.select('entries', where='id=$id AND owner=$user', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text, user):

    result = db.query("select MAX(id) as id from entries")
    newid = int(result[0].id) + 1
    db.insert('entries', id=newid, title=title, content=text, posted_on=datetime.datetime.utcnow(), owner=user)
    
def set_code(code, user):
    userdb.update('users', where="user=$user", vars=locals(),
        secretcode=code)
    
def del_post(id, user):
    db.delete('entries', where="id=$id AND owner=$user", vars=locals())

def update_post(id, title, text, user):
    db.update('entries', where="id=$id AND owner=$user", vars=locals(),
        title=title, content=text)

def transform_datestr(posted_on):
    datetime_obj = datetime.datetime.strptime(posted_on,'%Y-%m-%d %H:%M:%S.%f')
    return web.datestr(datetime_obj)

