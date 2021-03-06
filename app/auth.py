from functools import wraps
from app import db, lm
from flask import redirect, session, flash, url_for
from .forms import LoginForm
from models import User, Schools
from bcrypt import hashpw, gensalt
from flask.ext.login import login_user, logout_user

'''
Function that loads the user object. Used in the login_required func
'''
@lm.user_loader
def load_user(inp_username):
	u = User.objects(username = inp_username)

	if not u:
		return None
	return u[0].username

'''
Wrapper function that verifies that a user is logged in.
Method decorated with @login_required will not load unless a user is detected as "logged in"
'''
def login_required(f):
	'''
	Redirects to the log-in screen if the key "user_id" is not found
	Otherwise, hands control to the function it wrapped.

	EX:

	@login_required#This will execute if user_id exists
	def function(para,meters):
		...
		...

	otherwise, you get redirected to the login page
	'''
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'user_id' in session:
			flash('Hello, ', session['user_id'])
			return f(*args, **kwargs)
		else:
			flash('Please login!')
			return redirect(url_for('login'))
	return wrap

'''
Simple function that takes a username, password and email, and creates a user object in the DB
'''
def create_new_user(inp_username, inp_password, inp_email):
	#Save to the database the user with the above parameters
	U = User( email = inp_email, username = inp_username, hashed_pass = hashpw(password, gensalt()))
	U.save()

#You should get the user_id from the context!

'''
Functions that validate login, and extract hashed passwords
Password is verified via bcrypt's hashpw function. Quite intuitive!
'''
def extract_hashed_pw(query):
	return query.hashed_pass

def validate_login(password, password_hash, user):
	print(user.username)
	print("ATTEMPT: ", password, ' HASH: ', password_hash)
	return hashpw(password, password_hash) == password_hash
