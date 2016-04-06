from app import db
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

def extract_hashed_pw(queryList):
	if not queryList:
		return None
	else:
		return queryList[0].hashed_pass
def validate_login(password, password_hash):
	return hashpw(password, password_hash) == password_hash
