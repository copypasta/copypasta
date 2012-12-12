""" model module for copypasta online clipboard """
""" AppSec Fall 2012 """
""" George Ryabov, Kelvin Yang, David Chan, Anthony Candarini """
""" requires webpy 0.3 """

import web, datetime
import sqlite3
import re
db = web.database(dbn='sqlite', db='pasta.sqlite')
userdb = web.database(dbn='sqlite', db='users.sqlite')



#db.query("CREATE TABLE entries (id INT AUTO_INCREMENT, title TEXT, content TEXT, posted_on DATETIME, primary key (id));")

def get_clips(user):
    return db.select('entries', order='id DESC', where='owner=$user', vars=locals())

def set_owner(sessionid, user):
    db.update('entries', where="owner=$sessionid", vars=locals(),
        owner=user)

def get_id(user):
    return db.select('entries', order='id DESC', where='owner=$user', vars=locals())


def get_clip(id, user):
    try:
        return db.select('entries', where='id=$id AND owner=$user', vars=locals())[0]
    except IndexError:
        return None

def get_clip_public(publicid):
    try:
        return db.select('entries', where='publicid=$publicid', vars=locals())[0]
    except IndexError:
        return None

def get_latest(user):
    try:
        return db.select('entries', where='owner=$user',  order="posted_on DESC", limit=4, vars=locals())
    except IndexError:
        return None

def new_clip(title, text, user):

    result = db.query("select MAX(id) as id from entries")
    newid = int(result[0].id) + 1
    db.insert('entries', id=newid, title=title, content=text, posted_on=datetime.datetime.utcnow(), owner=user)

def set_code(code, user):
    timestamp = datetime.datetime.utcnow()
    userdb.update('users', where="user=$user", vars=locals(),
        secretcode=code, codecreated=datetime.datetime.utcnow())
    return timestamp

def del_clip(id, user):
    db.delete('entries', where="id=$id AND owner=$user", vars=locals())

def update_clip(id, title, text, user):
    db.update('entries', where="id=$id AND owner=$user", vars=locals(),
        title=title, content=text)


def share_clip(id, uniquid, user):
    db.update('entries', where="id=$id AND owner=$user", vars=locals(),
        publicid=uniquid)

def transform_datestr(posted_on):
    datetime_obj = datetime.datetime.strptime(posted_on,'%Y-%m-%d %H:%M:%S.%f')
    return web.datestr(datetime_obj)
