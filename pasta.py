""" main module for copypasta online clipboard """
""" AppSec Fall 2012 """
""" George Ryabov, Kelvin Yang, David Chan """
""" requires webpy 0.3 """
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
import model
from web import form
import hashlib, uuid
import json
import base64
from time import strftime

### Url mappings

urls = (
    '/', 'index',
    '/delete/(\d+)', 'delete',
    '/edit/(\d+)', 'edit',
    '/count', 'count',
    '/getcode', 'getcode',
    '/getcode/new', 'getnewcode',
    '/getclips', 'getclips',
    '/postclip', 'postclip',
    '/deleteclip', 'deleteclip',
    '/logout', 'logout',
    '/login', 'login', ###login page####
    '/signup', 'signup', ###sign up page####
)

#####added code for mysql useraccounts######
#db = web.database(dbn='mysql', db='users', user='useraccount', pw='useraccount1')
userdb = web.database(dbn='sqlite', db='users.sqlite')

app = web.application(urls, locals())
####needed for apache!
application = app.wsgifunc()
web.config.debug = False

curdir = os.path.dirname(__file__)

#session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')), initializer={'count': 0})
    web.config._session = session
else:
    session = web.config._session


if "session_id" not in session:
    session.session_id = "0"

####form for login####
loginform = form.Form(
	form.Textbox("username", form.notnull),
	form.Password("password", form.notnull))

####form for signup####
signupform = form.Form(
	form.Textbox('username', description="username:"),
	form.Password('password', description="password:"),
	form.Password('password_again', description="repeat password:"),
	validators = [form.Validator("Passwords didn't match.", lambda i: i.password == i.password_again)]
)

def loggedin():
    global session
    if 'loggedin' not in session:
        return False
    else:
        return session.loggedin

def getuser():
    global session
    if loggedin():
        return session.user
    elif "session_id" in session:
        return session.session_id
    else:
        return 0

def codecreated():
    global session
    if loggedin():
        if "codecreated" in session:
            return session.codecreated
        else:
            return ""
    else:
        return ""

### Templates
t_globals = {
    'datestr': model.transform_datestr,
    'loggedin':loggedin,
    'user':getuser
}
render = web.template.render('templates', base='base', globals= t_globals)

class index:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=15,
            description="Title:"),
        web.form.Textarea('content', web.form.notnull,
            rows=2, cols=15,
            description="Clipboard:"),
        web.form.Button('Save Clipboard'),
    )

    def GET(self):
        """ Show page """
        clips = model.get_clips(getuser())
        form = self.form()

        return render.index(clips, form)

    def POST(self):
        form = self.form()
        clips = model.get_clips(getuser())

        if not form.validates():
            return render.index(clips, form)

        model.new_clip(form.d.title, form.d.content, getuser())
        raise web.seeother('/')


class delete:

    def POST(self, id):
        model.del_clip(int(id), getuser())
        raise web.seeother('/')


class edit:

    def GET(self, id):
        clip = model.get_clip(int(id), getuser())
        if clip:
            form = index.form()
            form.fill(clip)
            return render.edit(clip, form)
        else:
            raise web.seeother('/')


    def POST(self, id):
        form = index.form()
        clip = model.get_clip(int(id), getuser())
        if clip:
            if not form.validates():
                return render.edit(clip, form)
            model.update_clip(int(id), form.d.title, form.d.content, getuser())
            raise web.seeother('/')
        else:
            raise web.seeother('/')

class count:
    def GET(self):
        if 'count' not in session:
            session.count = 0
        else:
            session.count += 1
        return str(session.count)

class reset:
    def GET(self):
        session.kill()
        return ""


###login class#####
class login:

    def GET(self):
        error = ""
        form = loginform()
        return render.login(form, error)

    def POST(self):
        global session
        error = ""
        form = loginform()
        if not form.validates():
            return render.login(form, error)
        else:

            try:
                userinfo = userdb.select('users', where='user=$form.d.username', vars=locals())

                userinfo = userinfo[0]

                password = userinfo.password
                salt = userinfo.salt

                hashed_password = hashlib.sha512(form.d.password + salt).hexdigest()

                if hashed_password == password:
                    print session.session_id
                    session.user = form.d.username
                    session.codecreated = userinfo.codecreated
                    session.loggedin = True
                    print session.session_id
                    model.set_owner(session.session_id, getuser())
                    raise web.seeother('/')
                else:
                    form = loginform()
                    error = "Login is invalid, please try again"
                    return render.login(form, error)
            except:
                form = loginform()
                error = "Login process failed"
                return render.login(form, error)

###login class#####
class logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')

####sign up class####

class signup:
    def GET(self):
        error = ""
        form = signupform()
        return render.signupform(form, error)

    def POST(self):
        form = signupform()
        if not form.validates():
            return render.signupform(form, "Please provide correct inputs")
        else:
            try:
                userdb.select('users', where='user=$form.d.username', vars=locals())[0]
                return render.signupform(form, "Username exists, pick a new one please")
            except:
                #create a secure password and store it
                newsalt = uuid.uuid4().hex
                hashed_password = hashlib.sha512(form.d.password + newsalt).hexdigest()

                userdb.insert('users', user=form.d.username, password=hashed_password, salt=newsalt, secretcode=str(uuid.uuid4()))

                session.user = form.d.username
                session.loggedin = True
                model.set_owner(session.session_id, getuser())
                raise web.seeother('/')

###login class#####
class getcode:
    def GET(self):
        global session
        if loggedin():
            code = codecreated()

            if str(code) == "" or str(code) == "None":
                code = str(uuid.uuid4())
                user = getuser()
                userinfo = userdb.select('users', where='user=$user', vars=locals())
                userinfo = userinfo[0]
                salt = userinfo.password
                hashed_secretcode = hashlib.sha512(code + salt).hexdigest()

                session.codecreated =  model.set_code(hashed_secretcode, getuser())
                return render.getcode(session.codecreated,"", True)
            else:
                return render.getcode(code,"", False)


        else:
            raise web.seeother('/')

class getnewcode:
    def GET(self):
        global session
        if loggedin():
            code = str(uuid.uuid4())

            user = getuser()
            userinfo = userdb.select('users', where='user=$user', vars=locals())
            userinfo = userinfo[0]
            salt = userinfo.password
            hashed_secretcode = hashlib.sha512(code + salt).hexdigest()

            session.codecreated = model.set_code(hashed_secretcode, getuser())
            return render.getcode(code,"", True)
        else:
            raise web.seeother('/')

class getclips:
    def GET(self):
        usercode =  web.ctx.env.get("HTTP_X_COPYPASTA_CODE")

        if usercode:

            split = usercode.split("&")
            user = split[0].split("=")[1]
            code = split[1].split("=")[1]

            if user:
                userinfo = userdb.select('users', where='user=$user', vars=locals())
                userinfo = userinfo[0]
                salt = userinfo.password

                hashed_secretcode = hashlib.sha512(code + salt).hexdigest()

                if hashed_secretcode == userinfo.secretcode:
                    clips = model.get_latest(user);
                    web.header('Content-Type', 'application/json')
                    return json.dumps(clips.list())
                else:
                    dict = {'status':"Bad login"}
                    web.header('Content-Type', 'application/json')
                    return json.dumps(dict)
            else:
                dict = {'status':"Invalid user"}
                web.header('Content-Type', 'application/json')
                return json.dumps(dict)
        else:
            raise web.seeother('/')

class postclip:
    def POST(self):
        usercode =  web.ctx.env.get("HTTP_X_COPYPASTA_CODE")

        if usercode:

            split = usercode.split("&")
            user = split[0].split("=")[1]
            code = split[1].split("=")[1]

            if user:
                userinfo = userdb.select('users', where='user=$user', vars=locals())
                userinfo = userinfo[0]
                salt = userinfo.password

                hashed_secretcode = hashlib.sha512(code + salt).hexdigest()

                if hashed_secretcode == userinfo.secretcode:
                    newclip = base64.b64decode(web.data())
                    model.new_clip("by " + user + " on " + strftime("%Y-%m-%d %H:%M"), newclip, user)
                    web.header('Content-Type', 'application/json')
                    dict = {'status':"Clip saved"}
                    return json.dumps(dict)
                else:
                    dict = {'status':"Bad login"}
                    web.header('Content-Type', 'application/json')
                    return json.dumps(dict)
            else:
                dict = {'status':"Invalid user"}
                web.header('Content-Type', 'application/json')
                return json.dumps(dict)
        else:
            raise web.seeother('/')

class deleteclip:
    def POST(self):
        usercode =  web.ctx.env.get("HTTP_X_COPYPASTA_CODE")

        if usercode:

            split = usercode.split("&")
            user = split[0].split("=")[1]
            code = split[1].split("=")[1]

            if user:
                userinfo = userdb.select('users', where='user=$user', vars=locals())
                userinfo = userinfo[0]
                salt = userinfo.password

                hashed_secretcode = hashlib.sha512(code + salt).hexdigest()

                if hashed_secretcode == userinfo.secretcode:
                    id = web.data()
                    print id;
                    if id:
                        model.del_clip(int(id), getuser())

                        web.header('Content-Type', 'application/json')
                        dict = {'status':"Clip deleted"}
                        return json.dumps(dict)
                    else:
                        dict = {'status':"Bad id"}
                        web.header('Content-Type', 'application/json')
                        return json.dumps(dict)
                else:
                    dict = {'status':"Bad login"}
                    web.header('Content-Type', 'application/json')
                    return json.dumps(dict)
            else:
                dict = {'status':"Invalid user"}
                web.header('Content-Type', 'application/json')
                return json.dumps(dict)
        else:
            raise web.seeother('/')

if __name__ == '__main__':

    app.run()
