from app import app, db
from flask import request, url_for, render_template, flash, redirect
from .forms import LoginForm, RegisterForm
from models import User
from auth import *
import unicodedata#for the pesky unicode stuff

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
	return render_template('index.html', title='Home', user=vessel, posts=posts)

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
	if request.method == 'POST' and form.validate_on_submit():
		user = User.objects(username=form.username.data)
		if not user:
			print("Something has gone horribly wrong")#TERMINATE EXECUTION HERE, Non-Existant user
		else:
			the_hash = extract_hashed_pass(user)#Retrieve the hashed_pass, user exists
	if validate_login(form.password.data, the_hash):#determine if the login is correct!
		user_obj = User.load_user(user)#get the username
		login_user(user_obj)
		flash("Logged in successfully", category='success')
		return redirect(request.args.get("next"))
	flash("Wrong username or password", category='error')

	return(render_template('login.html', form))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register/confirm', methods=['GET', 'POST'])
def register_confirm():
	form = RegisterForm()
	normalized_pass = unicodedata.normalize('NFKD', form.new_password.data).encode('ascii', 'ignore')
	new_user = User()

	normalized_name = unicodedata.normalize('NFKD', form.new_username.data).encode('ascii', 'ignore')

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
		unicode_vessel = unicodedata.normalize('NFKD', does_user_exist_now[0].username).encode('ascii', 'ignore')
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