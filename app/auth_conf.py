from app import app
from views import login_required, index
from flask import g, request, url_for, render_template, flash, redirect, session
from utils import normalize_from_unicode, setup_complete
from models import User
from auth import *
from algorithm_main import *
from normalize_func import *

'''
These functions handle login confirmation and logging out.
session is the user cookie session that flask creates for the user. Please do not disable cookies!!!!
'''

'''
login_confirm()
-This function takes in a username and password, verifies that the user is logged in,
and logs the user in once the proper conditions are met.
'''
@app.route('/')
@app.route('/login/confirm', methods=['GET', 'POST'])
#The parameters under methods specify what HTML reponses to accept
def login_confirm():

	#obtain data from form
	form_user_name = normalize_from_unicode(request.form['username'])
	form_password = normalize_from_unicode(request.form['password'])
	the_hash = '' #the good stuff

	#check if the request is html POST
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

	#This will verify if the password is correct. validate_login is in auth_conf
	if validate_login(form_password, normalize_from_unicode(the_hash), user):#determine if the login is correct!
		login_user(user, remember='no')
		session['logged_in'] = True
		session['username'] = form_user_name
		flash("Logged in successfully", category='success')
		#Stops the server from executing the fit number algorithm
		if setup_complete(form_user_name):
			pass
		else:
			return redirect(url_for('index'))
		#executes the fit algo
		print("running fit algorithm!")
		run_fit()#The fit number algorithm is executed here, located in algorithm_main
		return redirect(url_for('index'))

	flash("Wrong username or password", category='error')

	return redirect((url_for('index')))

'''
logout()
Logs out.
'''
@app.route('/')
@app.route('/logout')
@login_required
def logout():
	#Resets some cookie session info
	logout_user()
	session['logged_in'] = False
	session['username'] = None
	return redirect(url_for('index'))

'''
register_confirm()
upon registering, the user will send a request to flask in order to verify the new account.
'''
@app.route('/register/confirm', methods=['GET', 'POST'])
def register_confirm():
	#obtain data from the html form
	form = RegisterForm()
	normalized_pass = normalize_from_unicode(form.new_password.data)
	new_user = User()

	#normalize the data
	normalized_name = normalize_from_unicode(form.new_username.data)
	new_user.username = form.new_username.data
	new_user.email = form.new_email.data
	new_user.hashed_pass = hashpw(normalized_pass, gensalt())

	new_user.save()#Save the user after populating it with the new information

	#Simple sanity check to see if the user exists. Who knows?
	does_user_exist_now = User.objects(username=normalized_name)
	retrieved_name = ''
	if not does_user_exist_now:
		print("CATASTROPHIC ERROR")
		return redirect('registration.html', title='title', form=RegisterForm())
	else:
		#At this point the user is setup
		unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
		retrieved_name = unicode_vessel
		login_user(new_user, remember='no')
		flash("Logged in for the first time!", category='success')

	return render_template('index.html', title='LoggedIn')
