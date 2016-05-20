from app import app, db
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from auth import *
from utils import normalize_from_unicode, pull_random_schools#for the pesky unicode stuff
from flask.ext.login import current_user

@app.before_request
def before_request():
	g.user = current_user

'''
TEMPLATE FOR FRONT_END_DEVELOPERS!!!
@app.route('/')
@app.route('/the/url/you/want/the/browser/to/display')
def serve_html_page():
	#If some interstitial condition is not met (say, the context of a login is missing)
	#flash('') displays a message on the page 
	if some_condition_not_met:
		flash("message!") 
		return render("/Web_Development/PAGE_NAME.html", var="", ...)
	return render("/Web_Development/PAGE_NAME.html", var1="val", var2="val", ... )
'''

'''
Home page links! Anything that renders a template is here. Most things here return a page, instead of acting as an interstitial
method that flask requires for an action (form completion, login, etc.)g
'''
@app.route('/')
@app.route('/index')
def index():
	is_log = None
	if 'user_id' in session:
		print(session['user_id'])
		flash("Hello: ", normalize_from_unicode(session['user_id']))
	else:
		flash('Not logged in')

	if 'logged_in' in session:
		return redirect(url_for('return_dash'))

	return render_template('Web_Development/homepage.html', title='Home')

@app.route('/')
@app.route('/contacts_page')
def return_contact():
	return render_template('Web_Development/contact_us.html', title='Contact Us')

@app.route('/')
@app.route('/about')
def return_about():
	return render_template('Web_Development/about.html', title='About')

@app.route('/')
@app.route('/account_setup')
def return_account_setup():
	if 'user_id' not in session:
		return render_template('Web_Development/account_setup_0.html', title='Account Setup (Step 1 of 4)')
	else:
		return redirect(url_for('return_account_setup_1'))

@app.route('/')
@app.route('/account_setup_2')
@login_required
def return_account_setup_2():
	return render_template('Web_Development/account_setup_2.html', title="Account Setup (Step 3 of 4)")

@app.route('/')
@app.route('/account_setup_3')
@login_required
def return_account_setup_3():
	return render_template('Web_Development/account_setup_3.html', title="Account Setup (Step 4 of 4)")

@app.route('/')
@app.route('/account_setup_4')
@login_required
def return_account_setup_4():
	return render_template('Web_Development/account_setup_4.html', title="Account Setup Complete")

@app.route('/')
@app.route('/return_log')
def return_log():
	return render_template('Web_Development/login.html', title='Login')

@app.route('/settings')
@login_required
def settings():
	return render_template('settings.html')

@app.route('/')
@app.route('/register', methods=['GET'])
def register():
	form = RegisterForm()
	response = render_template('registration.html', title='title', form=form)
	return response

@app.route('/')
@app.route('/dashboard')
@login_required
def return_dash():
	school_obj1 = Schools()
	school_obj2 = Schools()
	school_obj3 = Schools()
	school_obj = pull_random_schools()
	return render_template('Web_Development/post_login.html', title='Dashboard', school=school_obj)
	
'''
Beyond this point are the //LOGOUT FUNCTIONS//
You'll find:
login(), login_confirm(), logout()
'''
@app.route('/')
@app.route('/login', methods=['GET'])
def login():
	form = LoginForm()
	response = render_template('Web_Development/login.html', title='title', form=form)
	return response

@app.route('/')
@app.route('/playground', methods=['GET'])
def get_playground():
	return render_template('Web_Development/playground.html')

@app.route('/')
@app.route('/playground/activate', methods=['POST'])
def do_playground_stuff():#This does some stuff
	field1 = normalize_from_unicode(request.form['FIELD1'])
	print('This is your input: ', field1)
	if field1 == 'TEST':
		print("hello!")
		return render_template('/Web_Development/playground.html')
	else:
		print("Whoops")

	return render_template('/Web_Development/playground.html')


@app.route('/')
@app.route('/randumb')
def randumb():
	school_obj = Schools()
	school_obj = pull_random_schools()
	print(school_obj.instnm)
	return render_template('Web_Development/school_temp.html')

from sign_up_views import *
from auth_conf import *

'''

PROTOTYPE FUNCTIONS. THESE ARE NOT FOR FINAL USE. MERELY A TEST
@app.route('/')
@app.route('/p_home')
def p_index():
	vessel = {'nickname': 'Miguel'} #fake user
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
	return render_template('index.html', title='Home', user=vessel, posts=posts)


!!DEBUG ZONE!! Everything here is a toy and is probably super useless
No documentation will probably ever be written for this stuff
'''