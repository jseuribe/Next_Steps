from flask import request, url_for, render_template, flash, redirect
from app import app, db
from .forms import LoginForm
from models import User
from auth import load_user, extract_hashed_pw, validate_login

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


@app.route('/login', methods=['GET', 'POST'])
#The parameters under methods specify what HTML reponses to accept
def login():
	form = LoginForm()
	the_hash = '' #the good stuff
	if request.method == 'POST' and form.validate_on_submit():
		user = User.objects(username=form.username.data)
		if not user:
			print("Something has gone horribly wrong")#TERMINATE EXECUTION HERE, Non-Existant user
		else:
			the_hash = extract_hashed_pass(user)#Retrieve the hashed_pass, user exists
	if validate_login(form.password.data, the_hash):#determine if the login is correct!
		user_obj = load_user(user)#get the username
			login_user(user_obj)
			flash("Logged in successfully", category='success')
			return redirect(request.args.get("next"))
	flash("Wrong username or password", category='error')

	return(render_template('login.html', title='login', form=form))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))