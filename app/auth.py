from app import db, lm
from flask import request, redirect, render_template, url_for, flash
from .forms import LoginForm
from models import User
from bcrypt import hashpw, gensalt
from flask.ext.login import login_user, logout_user


def create_new_user(inp_username, inp_password, inp_email):
	#Save to the database the user with the above parameters
	U = User( email = inp_email, username = inp_username, hashed_pass = hashpw(password, gensalt()))
	U.save()

#You should get the user_id from the context!

def extract_hashed_pw(query):
	return query.hashed_pass

def validate_login(password, password_hash, user):
	print(user.username)
	print("ATTEMPT: ", password, ' HASH: ', password_hash)
	return hashpw(password, password_hash) == password_hash

'''
def load_user(inp_username):
	u = User.objects(username = inp_username)

	if not u:
		return None
	return u[0].username
'''
@lm.user_loader
def load_user(inp_username):
	u = User.objects(username = inp_username)

	if not u:
		return None
	return u[0].username

