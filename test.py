import web
from web import form
render = web.template.render('templates/')

db = web.database(dbn='mysql', db='users', user='useraccount', pw='useraccount1')
urls = ('/', 'index',
	'/login', 'login',
	'/signup', 'signup',
	'/guest', 'guest',
)

app = web.application(urls, globals())

myform = form.Form( 
	form.Textbox("Username", form.notnull), 
	form.Password("Password", form.notnull))

mysignup = form.Form(
	form.Textbox('username'),
	form.Password('password'),
	form.Password('password_again'),
	validators = [form.Validator("Passwords didn't match.", lambda i: i.password == i.password_again)]
)

class index:
	def GET(self):
		return render.index()
class guest:
	def GET(self):
		return render.guest()
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
				db.insert('example_users', user=form.d.username, password=form.d.username)
				return "account created!"

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
			
	
			#ident = db.select('example_users', where='user=$form.d.Username', vars=locals())[0]
			#if hashlib.sha1("sAlT754-"+passwd).hexdigest() == ident['pass']:
			#	return "matches!"
	            # form.d.Username and form['Username'].value are equivalent ways of
	            # extracting the validated arguments from the form.
			#if (form.d.Username == "kyang"):
	            	#	return "Grrreat success! Username: %s, Password: %s" % (form.d.Username, form['Password'].value)
			#else:
			#	return "no match!"

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()