from app import app
from views import login_required, index
from flask import g, request, url_for, render_template, flash, redirect, session
from utils import normalize_from_unicode
from models import User
from auth import *
@app.route('/')
@app.route('/login/confirm', methods=['GET', 'POST'])
#The parameters under methods specify what HTML reponses to accept
def login_confirm():

	form_user_name = normalize_from_unicode(request.form['username'])
	form_password = normalize_from_unicode(request.form['password'])
	the_hash = '' #the good stuff

	if request.method == 'POST':
		user = User()
		user_set = User.objects(username=form_user_name)
		print("VALIDATING EXISTANCE HOLD ON")
		if not user_set:
			print("Something has gone horribly wrong")#TERMINATE EXECUTION HERE, Non-Existant user
			flash('Invalid user!')
			return redirect(url_for('return_log'))
		else:
			user = user_set[0]
			print("USERNAME")
			print(user.username)
			the_hash = user.hashed_pass#Retrieve the hashed_pass, user exists

	if validate_login(form_password, normalize_from_unicode(the_hash), user):#determine if the login is correct!
		login_user(user, remember='no')
		session['logged_in'] = True
		flash("Logged in successfully", category='success')
		return redirect(url_for('index'))

	flash("Wrong username or password", category='error')

	return redirect((url_for('index')))

@app.route('/')
@app.route('/logout')
@login_required
def logout():
	logout_user()
	session['logged_in'] = False
	return redirect(url_for('index'))

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
