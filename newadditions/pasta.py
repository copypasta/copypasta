""" Basic blog using webpy 0.3 """
import web
import model
from web import form

### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/count', 'Count',
    '/reset', 'Reset',
    '/login', 'login', ###login page####
    '/signup', 'signup', ###sign up page####
)


### Templates
t_globals = {
    'datestr': model.transform_datestr
}

#####added code for mysql useraccounts######
db = web.database(dbn='mysql', db='users', user='useraccount', pw='useraccount1')


app = web.application(urls, locals())
web.config.debug = False
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates', base='base', globals= t_globals)


####form for login####
myform = form.Form( 
	form.Textbox("Username", form.notnull), 
	form.Password("Password", form.notnull))

####form for signup####
mysignup = form.Form(
	form.Textbox('username'),
	form.Password('password'),
	form.Password('password_again'),
	validators = [form.Validator("Passwords didn't match.", lambda i: i.password == i.password_again)]
)


class Index:

    def GET(self):
        """ Show page """
        print session.session_id
        posts = model.get_posts()
        return render.index(posts)


class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return render.view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=15,
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull,
            rows=10, cols=80,
            description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


class Count:
    def GET(self):
        if 'count' not in session:
            session.count = 0
        else:
            session.count += 1
        return str(session.count)

class Reset:
    def GET(self):
        session.kill()
        return ""


###login class#####
class login: 
	def GET(self): 
	        form = myform()
	        # make sure you create a copy of the form by calling it (line above)
	        # Otherwise changes will appear globally
	        return render.formtest(form)

	def POST(self): 
	        form = myform() 
	        if not form.validates(): 
	            return render.formtest(form)
	        else:
			try:
				ident = db.select('example_users', where='user=$form.d.Username', vars=locals())[0]
				if form.d.Password == ident['password']:
					return "password matches"
				else:
					return "pasword no match"
			except:
				return "user does not exist"

####sign up class####

class signup:
	def GET(self):
		form = mysignup()
		return render.signupform(form)
	
	def POST(self):
		form = mysignup()
		if not form.validates(): 
	        	return render.signupform(form)
	        else:
			try:
				db.select('example_users', where='user=$form.d.username', vars=locals())[0]
				return "user exist already!"
			except:
				db.insert('example_users', user=form.d.username, password=form.d.password)
				return "account created!"


if __name__ == '__main__':

    app.run()