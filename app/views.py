from app import app, db, pymon
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from auth import *
from utils import normalize_from_unicode, pull_random_schools, resolve_school_objid, find_school_by_name, isbookmarked#for the pesky unicode stuff
from utils import extract_bookmarks
from flask.ext.login import current_user
import string
from bson import ObjectId


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
	print("Determining which homepage to return")
	if 'user_id' in session:
		print(session['user_id'])
		flash("Hello: ", normalize_from_unicode(session['user_id']))
	else:
		flash('Not logged in')

	if 'logged_in' in session:
		print('checking if logged')
		if session['logged_in']:
			return redirect(url_for('return_dash'))
	else:
		print('Not logged in at all!')
		return render_template('Web_Development/homepage.html', title='Home')
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
@app.route('/privacy')
def return_privacy():
	return render_template('Web_Development/privacy.html', title='Privacy Policy')

@app.route('/')
@app.route('/terms')
def return_terms():
	return render_template('Web_Development/terms.html', title='Terms of Service')

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
	print("returning dashboard")
	school_obj1 = Schools()
	school_obj2 = Schools()
	school_obj3 = Schools()
	school_obj1 = find_school_by_name("CUNY Hunter College")
	school_obj2 = find_school_by_name("Columbia University in the City of New York")
	school_obj3 = find_school_by_name("Stony Brook University")
	print(school_obj1.instnm)
	s_list = [school_obj1, school_obj2, school_obj3]
	return render_template('Web_Development/post_login.html', title='Dashboard', school_list=s_list)
	
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

'''
Test functions for checking how flask's parameter sending works.
'''

@app.route('/')
@app.route('/randumb')
def randumb():
	school_obj = Schools()
	school_obj = pull_random_schools()
	print(school_obj.instnm)
	return render_template('Web_Development/school_temp.html')

@app.route('/')
@app.route('/schoolpage')
@app.route('/schoolpage/<string:school_objid>')
def param_test(school_objid=None):
	print(school_objid)
	school_object = resolve_school_objid(school_objid)
	return render_template('Web_Development/school_profile.html', school=school_object)

@app.route('/')
@app.route('/bookmarks')
@login_required
def return_bookmarks():
	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_q = User.objects(username=u_name_look_up) #get the object

	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_1'))

	user_obj = user_q[0]#This should be the object what is the user.
	school_bookmarks = user_obj.bookmarks

	school_list = extract_bookmarks(school_bookmarks)
	print(school_list)
	for school in school_list:
		print(school.instnm)
	return render_template('Web_Development/bookmarked_schools.html', bookmarks=school_list)

from sign_up_views import *
from auth_conf import *

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

		is_marked = not isbookmarked(school_objid, user_bookmarks)
		if is_marked:

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
			return render_template('Web_Development/school_temp.html')
	return render_template('Web_Development/school_temp.html')


@app.route('/')
@app.route('/accepted_to')
@app.route('/accepted_to/<string:school_objid>')
@login_required
def accepted_to_school(school_objid=None):
	from models import Schools
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
	#Find the User
	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.
	major_list = request.form.getlist('majors')

	user_cursor = pymon.db.user.find({'username': u_name_look_up})
	user_result = user_cursor.count()
	user_id = ""
	if user_result == 0:
		print("Error! No user found?")
		return redirect(url_for('index'))#Handle this later
	else:
		print("User id is found")
		for record in user_cursor:
			user_id = str(record[u'_id'])#obtain the user's object ID

	print('user id: ', user_id)
	#Find the School, obtain the list of accepted students, and add them to the list of accepted students
	print("Find school by id")
	print(school_objid)
	cursor_list = pymon.db.school.find({"_id": ObjectId(school_objid) })
	query_result = cursor_list.count()
	if query_result == 0:
		print("Error! No school")
		return redirect(url_for('index'))#Handle this later
	new_school = Schools()
	accepted_list = []#Empty list.
	for record in cursor_list:
		print("User will now be added to the list of users")
		if 'accepted_students' in record:#check if the school has a list of accepted students
			print("Field exist")
			accepted_list = record['accepted_students']#obtain an object id for lookup purposes
		else:
			print("Field does not exists")
			pymon.db.school.update({u"_id": ObjectId(school_objid) }, {'$set' : {u'accepted_students': []}})
		accepted_list.append(user_id)#Append the student to the list, either starting the list or adding to the list.
		print("Printing new list")
		print(accepted_list)
		pymon.db.school.update({'_id': school_objid}, {'$addToSet': {'accepted_students': user_id}})

	print("CONFIRMATION---------------------------")
	confirm_list_cursor = pymon.db.school.find({"_id": ObjectId(school_objid) })
	for record in confirm_list_cursor:
		print(record)
		print(record['accepted_students'])
	return return_bookmarks()



'''
Mongo find_by_id db.user.find({"_id" : ObjectId("573fdc635aeffc16e6ca6c83"}).pretty()
'''
