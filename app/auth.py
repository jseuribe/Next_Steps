from app import app
from app import db, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user
from .forms import LoginForm
from models import User
from bcrypt import hashpw, gensalt

def create_new_user(inp_username, inp_password, inp_email):
	#Save to the database the user with the above parameters
	U = User( email = inp_email, username = inp_username, hashed_pass = hashpw(password, gensalt()))
	U.save()

#You should get the user_id from the context!

@lm.user_loader
def load_user(inp_id):
	u = User.objects(user_id = inp_id)

	if not u:
		return None
	return User(u['user_id'])

def validate_login(password, password_hash):
	return hashpw(password, password_hash) == password_hash