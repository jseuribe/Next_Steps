from app import app, db
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from models import User
from auth import *
from utils import normalize_from_unicode#for the pesky unicode stuff
from flask.ext.login import current_user

@app.before_request
def before_request():
	g.user = current_user

'''
TEMPLATE FOR FRONT_END_DEVELOPERS!!!
@app.route('/')
@app.route('/the/url/you/want/the/browser/to/display')
def serve_html_page():
	#If some interstitial condition is not met (say, the context of a login is missing)
	#flash('') displays a message on the page 
	if some_condition_not_met:
		flash("message!") 
		return render("/Web_Development/PAGE_NAME.html", var="", ...)
	return render("/Web_Development/PAGE_NAME.html", var1="val", var2="val", ... )
'''

'''
Home page links! Anything that you can get to from the homepage is here
Includes: Homepage, Contacts, About, and Account_Setup.
'''
@app.route('/')
@app.route('/index')
def index():
	vessel = {'nickname': 'Miguel'} #fake user
	posts = [
		{
			'author': {'nickname': 'John'},
			'body':	'Beautiful day in City 17!'
		},

		{
			'author': {'nickname': 'Susan'},
			'body': 'The Avengers movie was so cool! Shame about Batman Vs. Superman!'
		}
	]
	return render_template('Web_Development/homepage.html', title='Home', user=vessel, posts=posts)

@app.route('/')
@app.route('/contacts_page')
def return_contact():
	return render_template('Web_Development/contact_us.html')

@app.route('/')
@app.route('/about')
def return_about():
	return render_template('Web_Development/about.html')

@app.route('/')
@app.route('/account_setup')
def return_account_setup():
	return render_template('Web_Development/account_setup_0.html')

@app.route('/')
@app.route('/return_log')
def return_log():
	return render_template('Web_Development/login.html')

@app.route('/settings')
@login_required
def settings():
	return render_template('settings.html')

@app.route('/')
@app.route('/register', methods=['GET'])
def register():
	form = RegisterForm()
	response = render_template('registration.html', title='title', form=form)
	return response

'''
Beyond this point are the //LOGOUT FUNCTIONS//
You'll find:
login(), login_confirm(), logout()
'''
@app.route('/')
@app.route('/login', methods=['GET'])
def login():
	form = LoginForm()
	response = render_template('login.html', title='title', form=form)
	return response

@app.route('/')
@app.route('/login/confirm', methods=['GET', 'POST'])
#The parameters under methods specify what HTML reponses to accept
def login_confirm():

	form = LoginForm()
	the_hash = '' #the good stuff

	if request.method == 'POST':
		user = User()
		user_set = User.objects(username=normalize_from_unicode(form.username.data))
		print("VALIDATING EXISTANCE HOLD ON")
		if not user_set:
			print("Something has gone horribly wrong")#TERMINATE EXECUTION HERE, Non-Existant user
			flash('Invalid user!')
			return redirect(url_for('login'))
		else:
			user = user_set[0]
			print("USERNAME")
			print(user.username)
			the_hash = user.hashed_pass#Retrieve the hashed_pass, user exists

	if validate_login(normalize_from_unicode(form.password.data), normalize_from_unicode(the_hash), user):#determine if the login is correct!
		login_user(user, remember='no')
		flash("Logged in successfully", category='success')
		return render_template('success.html')

	flash("Wrong username or password", category='error')

	return(render_template('login.html', form))

@app.route('/')
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register/confirm', methods=['GET', 'POST'])
def register_confirm():
	form = RegisterForm()
	normalized_pass = normalize_from_unicode(form.new_password.data)
	new_user = User()

	normalized_name = normalize_from_unicode(form.new_username.data)

	new_user.username = form.new_username.data
	'''
	if not new_user.username:
		flash("Invalid username", category='success')
		return render_template('{{url_for("register")}}', title='title', form=RegisterForm())
	'''
	new_user.email = form.new_email.data
	'''
	if not new_user.email:
		flash("Invalid email", category='success')
		return render_template('register.html', title='title', form=RegisterForm())
	'''
	new_user.hashed_pass = hashpw(normalized_pass, gensalt())
	'''
	if not new_user.hashed_pass:
		flash("Invalid password", category='success')
		return render_template('{{url_for("register")}}', title='title', form=RegisterForm())
	'''
	new_user.save()#Save the user after populating it with the new information

	does_user_exist_now = User.objects(username=normalized_name)
	retrieved_name = ''
	if not does_user_exist_now:
		print("CATASTROPHIC ERROR")
		return redirect('registration.html', title='title', form=RegisterForm())
	else:
		unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
		retrieved_name = unicode_vessel
		login_user(new_user, remember='no')
		flash("Logged in for the first time!", category='success')

	#Begin bad validation
	user = {'nickname': retrieved_name} #display a new name!
	posts = [
		{
			'author': {'nickname': 'John'},
			'body':	'Beautiful day in portland!'
		},

		{
			'author': {'nickname': 'Susan'},
			'body': 'The Avengers movie was so cool! Shame about BvS!'
		}
	]
	#End bad validation
	return render_template('index.html', title='LoggedIn', user=user, post=posts)

'''
If the html page that uses the action "account_setup"
calls this method with the form:

<form action='/account_setup' method='POST'>
	<label for ='FIELD1'>FIELD1: </label>
	<input type='text' name='FIELD1" /> <br />
	<input type='submit'/>
</form>

Then your method should look like:

@app.route('/account_setup', methods=['POST'])
def account_setup():
	FIELD1 = request.form['FIELD1'] #Should obtain FIELD1

'''
@app.route('/')
@app.route('/account_setup')
def account_setup():
	return True

'''
PROTOTYPE FUNCTIONS. THESE ARE NOT FOR FINAL USE. MERELY A TEST
'''
@app.route('/')
@app.route('/p_home')
def p_index():
	vessel = {'nickname': 'Miguel'} #fake user
	posts = [
		{
			'author': {'nickname': 'John'},
			'body':	'Beautiful day in portland!'
		},

		{
			'author': {'nickname': 'Susan'},
			'body': 'The Avengers movie was so cool! Shame about BvS!'
		}
	]
	return render_template('index.html', title='Home', user=vessel, posts=posts)


'''
!!DEBUG ZONE!! Everything here is a toy and is probably super useless
No documentation will probably ever be written for this stuff
'''
@app.route('/')
@app.route('/playground', methods=['GET'])
def get_playground():
	return render_template('Web_Development/playground.html')

@app.route('/')
@app.route('/playground/activate', methods=['POST'])
def do_playground_stuff():#This does some stuff
	field1 = normalize_from_unicode(request.form['FIELD1'])
	print('This is your input: ', field1)
	if field1 == 'TEST':
		print("hello!")
		return render_template('/Web_Development/playground.html')
	else:
		print("Whoops")

	return render_template('/Web_Development/playground.html')

'''
"""
function register() handles registration once called from the appropriate action form in
account_setup.html.

Currently this expects only 5 fields (password & pass verification, email, first and last names)
This can be easily expanded to receive other input as we see fit, or it can be separated into other fields
"""
@app.route('/')
@app.route('/register', methods=['POST'])
def register():
	#Obtain some initial information from the request form

	password = normalize_from_unicode(request.form['password'])
	verify_password = normalize_from_unicode(request.form['verify_passord'])

	email = normalize_from_unicode(request.form['email'])

	f_name = normalize_from_unicode(request.form['f_name'])
	l_name = normalize_from_unicode(request.form['l_name'])
	
	#Other fields will probably be squeezed in here. Or perhaps in another function?

	#include a check for if password == verify_password
	if not password && not verify_password && not email && not f_name && not l_name:
		print("CRITICAL ERROR")
	else:
		#normal execution
		#Initialize the basic profile info to this other information
		new_user = User()
		new_user.username = email #Are user-names required?
		new_user.email = email
		new_user.hashed_pass = hashpw(password, gensalt())
		new_user.save()#Save the user after populating it with the new information

		does_user_exist_now = User.objects(username=normalized_name)
		retrieved_name = ''
		if not does_user_exist_now:#Not sure when this could happen. But good to check otherwise
			print("CATASTROPHIC ERROR")
			return redirect('{{url_for("account_setup.html")}}')
		else:#The object is correct! Now create a new context and log the new user in
			unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
			retrieved_name = unicode_vessel
			login_user(new_user, remember='no')
			flash("Logged in for the first time!", category='success')

	return render_template('{{url_for('index')}}')


'''

@app.route('/')
@app.route('/account_setup_0/confirm', methods=['POST'])
def account_setup_0():

	if 'user_id' in session:
		flash('You are logged in already!')
		return render_template('Web_Development/account_setup_1.html')
	else:
		n_username = normalize_from_unicode(request.form['email'])
		n_email = normalize_from_unicode(request.form['email'])
		n_passw = normalize_from_unicode(request.form['password'])
		n_v_passw = normalize_from_unicode(request.form['v_password'])

		if not n_username and not n_email and not n_passw and not n_v_passw:
			flash("error, please do not leave any field blank")
			return render_template('/Web_Development/account_setup_0.html')
		elif n_passw != n_v_passw:
			flash("Passwords do not match, re-enter both")
			return render_template('/Web_Development/account_setup_0.html')
		else:
			new_user = User()
			new_user.email = n_email
			new_user.username = n_username
			new_user.hashed_pass = hashpw(n_passw, gensalt())
			new_user.save()
			does_user_exist_now = User.objects(username=n_username)
			if not does_user_exist_now:
				flash('Something went wrong; please try again.')
				return render_template('Web_Development/account_setup_0.html')
			else:#The object is correct!
				unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
				retrieved_name = unicode_vessel
				login_user(new_user, remember='no')
				flash("Logged in for the first time!, category='success'")

	return render_template('Web_Development/account_setup_1.html')

@app.route('/')
@app.route('/account_setup_1', methods=['GET'])
@login_required
def return_account_setup_1():
	return render_template('Web_Development/account_setup_1')

@app.route('/')
@app.route('/account_setup_1/confirm')
@login_required
def account_setup_1():
	n_f_name = normalize_from_unicode(request.form['f_name'])
	n_m_name = normalize_from_unicode(request.form['m_name'])
	n_l_name = normalize_from_unicode(request.form['l_name'])
	n_street = normalize_from_unicode(request.form['street'])

	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_q = User.objects(username=u_name_look_up) #get the object


