from app import app, db
from flask import request, url_for, render_template, flash, redirect
from .forms import LoginForm, RegisterForm
from models import *
from auth import *

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Miguel'} #fake user
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
	return render_template('index.html', title='Home', user=user, posts=posts)

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
	new_user = User(username=form.new_username.data, email=form.new_email.data, hashed_pass=hashpw(form.new_password.data, gensalt()))
	new_user.save()#Save the user after populating it with the new information

	u_obj = User.load_user(form.new_username.data)
	if not u_obj:
		print("CATASTROPHIC ERROR")
		return redirect('registration.html', title='title', form=RegisterForm())
	else:
		login_user(u_obj)
		flash("Logged in for the first time!", category='success')

	#Begin bad validation
	user = {'nickname': form.new_username.data} #display a new name!
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