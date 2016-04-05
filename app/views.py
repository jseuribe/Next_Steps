from flask import request, url_for, render_template, flash, redirect
from app import app, db
from .forms import LoginForm
from models import User

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

	if request.method == 'POST' and form.validate_on_submit():
		user = User.objects(username=form.username.data)
	if user and User.v