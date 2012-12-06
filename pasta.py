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

### Url mappings

urls = (
    '/', 'index',
    '/delete/(\d+)', 'delete',
    '/edit/(\d+)', 'edit',
    '/count', 'count',
    '/getcode', 'getcode',
    '/logout', 'logout',
    '/login', 'login', ###login page####
    '/signup', 'signup', ###sign up page####
)

#####added code for mysql useraccounts######
#db = web.database(dbn='mysql', db='users', user='useraccount', pw='useraccount1')
userdb = web.database(dbn='sqlite', db='users.sqlite')

app = web.application(urls, locals())
web.config.debug = False

curdir = os.path.dirname(__file__)

session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')), initializer={'count': 0})
#session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
web.config._session = session

####needed for apache!
application = app.wsgifunc()

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
    global session;
    if 'loggedin' not in session:
        return False;
    else:
        return session.loggedin;

def user():
    global session;
    if loggedin():
        return session.user;
    elif "session_id" in session:
        return session.session_id;
    else:
        return 0;
        
### Templates
t_globals = {
    'datestr': model.transform_datestr,
    'loggedin':loggedin,
    'user':user
}
render = web.template.render('templates', base='base', globals= t_globals)


class index:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=15,
            description="Title:"),
        web.form.Textarea('content', web.form.notnull,
            rows=2, cols=40,
            description="Clipboard:"),
        web.form.Button('Save Clipboard'),
    )

    def GET(self):
        """ Show page """
        posts = model.get_posts(user())
        form = self.form()

        #print session.session_id

        return render.index(posts, form)

    def POST(self):
        form = self.form()
        posts = model.get_posts(user())
        if not form.validates():
            return render.index(posts, form)
        model.new_post(form.d.title, form.d.content, user())
        raise web.seeother('/')

class delete:

    def POST(self, id):
        model.del_post(int(id), user())
        raise web.seeother('/')


class edit:

    def GET(self, id):
        post = model.get_post(int(id), user())
        form = index.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = index.form()
        post = model.get_post(int(id), user())
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content, user())
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
                    session.user = form.d.username
                    session.loggedin = True
                    model.set_owner(session.session_id, user())
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

                userdb.insert('users', user=form.d.username, password=hashed_password, salt=newsalt)

                session.user = form.d.username
                session.loggedin = True
                model.set_owner(session.session_id, user())
                raise web.seeother('/')

###login class#####
class getcode:
    def GET(self):
        if loggedin():
            return render.getcode()
        else:
            raise web.seeother('/')
        #session.loggedin = False
        #raise web.seeother('/')

        
if __name__ == '__main__':

    app.run()
