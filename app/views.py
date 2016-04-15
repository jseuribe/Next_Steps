from app import app, db
from flask import g, request, url_for, render_template, flash, redirect
from .forms import LoginForm, RegisterForm
from models import User
from auth import *
from utils import normalize_from_unicode#for the pesky unicode stuff
from flask.ext.login import current_user

@app.before_request
def before_request():
	g.user = current_user


@app.route('/')
@app.route('/index')
def index():
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
	return render_template('Web_Development/homepage.html', title='Home', user=vessel, posts=posts)

@app.route('/')
@app.route('/about')
def return_about():
	return render_template('Web_Development/about.html')
	
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
	new_user.email = form.new_email.data
	new_user.hashed_pass = hashpw(normalized_pass, gensalt())
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