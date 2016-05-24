from app import app, db
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from auth import *
from utils import normalize_from_unicode, pull_random_schools, resolve_school_objid, find_school_by_name#for the pesky unicode stuff
from flask.ext.login import current_user
import string

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
		return render("/PAGE_NAME.html", var="", ...)
	return render("/PAGE_NAME.html", var1="val", var2="val", ... )
'''

'''
Home page links! Anything that renders a template is here. Most things here return a page, instead of acting as an interstitial
method that flask requires for an action (form completion, login, etc.)g
'''
@app.route('/')
@app.route('/index')
def index():
	if 'user_id' in session:
		print(session['user_id'])
		flash("Hello: ", normalize_from_unicode(session['user_id']))
	else:
		flash('Not logged in')

	if not 'logged_in' in session or session['logged_in']:
		return redirect(url_for('return_dash'))
	else:
		return render_template('/homepage.html', title='Home')

@app.route('/')
@app.route('/contacts_page')
def return_contact():
	return render_template('/contact_us.html', title='Contact Us')

@app.route('/')
@app.route('/about')
def return_about():
	return render_template('/about.html', title='About')

@app.route('/')
@app.route('/account_setup')
def return_account_setup():
	if 'user_id' not in session:
		return render_template('/account_setup_0.html', title='Account Setup (Step 1 of 4)')
	else:
		return redirect(url_for('return_account_setup_1'))

@app.route('/')
@app.route('/account_setup_2')
@login_required
def return_account_setup_2():
	return render_template('/account_setup_2.html', title="Account Setup (Step 3 of 4)")

@app.route('/')
@app.route('/account_setup_3')
@login_required
def return_account_setup_3():
	return render_template('/account_setup_3.html', title="Account Setup (Step 4 of 4)")

@app.route('/')
@app.route('/account_setup_4')
@login_required
def return_account_setup_4():
	return render_template('/account_setup_4.html', title="Account Setup Complete")

@app.route('/')
@app.route('/return_log')
def return_log():
	return render_template('/login.html', title='Login')

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
	print("returning dashboard")
	school_obj1 = Schools()
	school_obj2 = Schools()
	school_obj3 = Schools()
	school_obj1 = find_school_by_name("CUNY Hunter College")
	school_obj2 = find_school_by_name("Columbia University in the City of New York")
	school_obj3 = find_school_by_name("Stony Brook University")
	print(school_obj1.instnm)
	s_list = [school_obj1, school_obj2, school_obj3]
	return render_template('/post_login.html', title='Dashboard', school_list=s_list)
	
'''
Beyond this point are the /LOGOUT FUNCTIONS/
You'll find:
login(), login_confirm(), logout()
'''
@app.route('/')
@app.route('/login', methods=['GET'])
def login():
	form = LoginForm()
	response = render_template('/login.html', title='title', form=form)
	return response

@app.route('/')
@app.route('/playground', methods=['GET'])
def get_playground():
	return render_template('/playground.html')

@app.route('/')
@app.route('/playground/activate', methods=['POST'])
def do_playground_stuff():#This does some stuff
	field1 = normalize_from_unicode(request.form['FIELD1'])
	print('This is your input: ', field1)
	if field1 == 'TEST':
		print("hello!")
		return render_template('/playground.html')
	else:
		print("Whoops")

	return render_template('/playground.html')

'''
Test functions for checking how flask's parameter sending works.
'''

@app.route('/')
@app.route('/randumb')
def randumb():
	school_obj = Schools()
	school_obj = pull_random_schools()
	print(school_obj.instnm)
	return render_template('/school_temp.html')

@app.route('/')
@app.route('/schoolpage')
@app.route('/schoolpage/<string:school_objid>')
def param_test(school_objid=None):
	print(school_objid)
	school_object = resolve_school_objid(school_objid)
	return render_template('/school_profile.html', school=school_object)

from sign_up_views import *
from auth_conf import *

def isbookmarked(string_objid, bookmark_list):
	norm_test_objid = normalize_from_unicode(string_objid)
	norm_test_objid = ''.join(filter(lambda c: c in string.printable, norm_test_objid))
	for item in bookmark_list:
		current_objid = item[0]#Get the current bookmark
		norm_item_objid = normalize_from_unicode(current_objid)
		norm_item_objid = ''.join(filter(lambda c: c in string.printable, norm_item_objid))

		print("checking", norm_item_objid, " against: ", norm_test_objid)
		print("length of item: ", len(norm_item_objid), "  len of query: ", len(norm_test_objid))
		print(type(norm_test_objid), type(norm_test_objid))
		if norm_item_objid is norm_test_objid:
			print("in your bookmarks")
			return True
		elif not norm_test_objid is norm_item_objid:
			print("Not in your bookmarks")
			continue
	return False

@app.route('/')
@app.route('/addbookmark/<string:school_objid>')
@login_required
def add_bookmark(school_objid=None):
	current_user_cursor = User.objects(username=session['username'])
	if not current_user_cursor:
		return render_template(url_for('return_dash'))
	else:
		current_user = current_user_cursor[0] #obtain the user
		user_bookmarks = current_user.bookmarks #retrieve a simple thing of lists from the mongo user document

		if not isbookmarked(school_objid, user_bookmarks):

			school_query = resolve_school_objid(school_objid)#Find the school object (existence verification)

			if not school_query:#Verify that our school is in our database
				print('school not found!')
				return render_template(url_for('param_test', school_objid))#redirect the user to the school page they were on.
			else:
				school_name = school_query.id_num #Obtain the id for storage
				acceptance_status = 'NoR'#Set default status No-Reply (Pre acceptance/notification from school)
				pair = []
				pair.append(school_name)
				pair.append(acceptance_status)

				user_bookmarks.append(pair)#Add to the pair, the next step will be adding to the mongoDB
				current_user.bookmarks = user_bookmarks
				current_user.save()
		else:
			print("Already bookmarked!")
			return render_template('/school_temp.html')
	return render_template('/school_temp.html')
