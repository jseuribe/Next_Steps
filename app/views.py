from flask import request, url_for, render_template, flash, redirect
from app import app, db
from .forms import LoginForm
from models import User
from auth import validate_login

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
			print("Something has gone horribly wrong")
		else:
			the_hash = user.hashed_pass#Retrieve the hashed_pass
	if user and validate_login(form.password.data, the_hash):
		user_obj = user.user_id#get the user id
			login_user(user_obj)
			flash("Logged in successfully", category='success')
			return redirect(request.args.get("next"))
	flash("Wrong username or password", category='error')

	return(render_template('login.html', title='login', form=form))