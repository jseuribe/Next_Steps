from app import app, db, pymon
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from auth import *
from utils import normalize_from_unicode, pull_random_schools, resolve_school_objid, find_school_by_name, isbookmarked#for the pesky unicode stuff
from utils import extract_bookmarks, setup_complete
from flask.ext.login import current_user
import string
from bson import ObjectId
import operator
from algorithm_main import *
from normalize_func import *

'''
PURPOSE: This file holds the bulk of the simple functions that return the html pages
And the bulk of the user interface system
'''

#Obtains the user info before a request is made
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
method that flask requires for an action (form completion, login, etc.)
'''

'''
index controls what page to display once a user clicks go-to homepage.
This is controlled by session data (what setup phase they left in)
By what their progress_setup data field is, if logged in.
Or if they're logged in or not
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
		if setup_complete(session['username']):
			return redirect(url_for('return_dash'))
		print('checking if logged')
		if session['logged_in']:
			if 'completion' in session:
				if session['completion'] == '1':
					return redirect(url_for('return_account_setup_1'))
				elif session['completion'] == '2':
					return redirect(url_for('return_account_setup_2'))
				elif session['completion'] == '3':
					return redirect(url_for('return_account_setup_3'))
			elif not 'completion' in session:
				if setup_complete(session['username']):
					return redirect(url_for('return_dash'))
				else:
					return redirect(url_for('return_account_setup_1'))
			elif session['completion'] == 'complete' or setup_complete():
				return redirect(url_for('return_dash'))
	else:
		print('Not logged in at all!')
		return render_template('Web_Development/homepage.html', title='Home')		
	return render_template('Web_Development/homepage.html', title='Home')

'''


Some simple one line functions that handle html retrieval


'''
#Return contacts page
@app.route('/')
@app.route('/contacts_page')
def return_contact():
	return render_template('Web_Development/contact_us.html', title='Contact Us')

#Return about
@app.route('/')
@app.route('/about')
def return_about():
	return render_template('Web_Development/about.html', title='About')
	
#return privacy
@app.route('/')
@app.route('/privacy')
def return_privacy():
	return render_template('Web_Development/privacy.html', title='Privacy Policy')

#return terms(they're binding) U can't sue us :^)
@app.route('/')
@app.route('/terms')
def return_terms():
	return render_template('Web_Development/terms.html', title='Terms of Service')

'''
Some functions that return account setup
'''
#Return the first account setup page(password and username)
@app.route('/')
@app.route('/account_setup')
def return_account_setup():
	if 'user_id' not in session:
		return render_template('Web_Development/account_setup_0.html', title='Account Setup (Step 1 of 4)')
	else:
		return redirect(url_for('return_account_setup_1'))

#Return the second account setup page (name and address)
@app.route('/')
@app.route('/account_setup_2')
@login_required
def return_account_setup_2():
	return render_template('Web_Development/account_setup_2.html', title="Account Setup (Step 3 of 4)")

#Return the third acc setup page (school and grade info)
@app.route('/')
@app.route('/account_setup_3')
@login_required
def return_account_setup_3():
	return render_template('Web_Development/account_setup_3.html', title="Account Setup (Step 4 of 4)")

#Return the completion
@app.route('/')
@app.route('/account_setup_4')
@login_required
def return_account_setup_4():
	run_fit()
	return render_template('Web_Development/account_setup_4.html', title="Account Setup Complete")

#Return the login screen
@app.route('/')
@app.route('/return_log')
def return_log():
	return render_template('Web_Development/login.html', title='Login')

#Return settings?
'''
@app.route('/settings')
@login_required
def settings():
	return render_template('settings.html')
'''

#return the register page
@app.route('/')
@app.route('/register', methods=['GET'])
def register():
	form = RegisterForm()
	response = render_template('registration.html', title='title', form=form)
	return response

'''
Return the dashboard

The dashboard is the page users view when they log in

'''
@app.route('/')
@app.route('/dashboard')
@login_required
def return_dash():
	print("returning dashboard")
	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_cursor = pymon.db.user.find({'username': u_name_look_up})
	user_result = user_cursor.count()
	first = ""
	last = ""
	fit_list = {}
	top3 = {}
	if user_result == 0:
		print("User not found?")
	for record in user_cursor:
		fit_list = dict(record['recommended_schools'])
		first = record['f_name']
		last = record['l_name']
		top3 = dict(sorted(fit_list.iteritems(), key=operator.itemgetter(1), reverse=True)[:7])

	key_three = list(top3.keys())
	s_list = []
	for key in key_three:
		s_list.append(find_school_by_name(key, fit_list))
	return render_template('Web_Development/post_login.html', title='Dashboard', school_list=s_list, f_name=first, l_name=last)
	
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

'''
Render the school page object.
'''
@app.route('/')
@app.route('/schoolpage')
@app.route('/schoolpage/<string:school_objid>')
def param_test(school_objid=None):
	print(school_objid)
	school_object = resolve_school_objid(school_objid)
	return render_template('Web_Development/school_profile.html', school=school_object)

'''
Display the bookmark list
'''
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
	school_bookmarks = user_obj.bookmarks#And this is the user's bookmark list

	school_list = extract_bookmarks(school_bookmarks)
	print(school_list)
	for school in school_list:
		print(school.instnm)
	return render_template('Web_Development/bookmarked_schools.html', bookmarks=school_list)

from sign_up_views import *
from auth_conf import *

'''
Add a bookmark
'''
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
			return redirect(url_for('return_bookmarks'))
	return redirect(url_for('return_bookmarks'))


'''
Mark a school as accepted
'''
@app.route('/')
@app.route('/accepted_to')
@app.route('/accepted_to/<string:school_objid>')
@login_required
def accepted_to_school(school_objid=None):
	from models import Schools
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
		pymon.db.school.update({'_id': ObjectId(school_objid)}, {'$addToSet': {'accepted_students': session['user_id']}})
		#The user is now in the list of accepted user for the school
	print("CONFIRMATION---------------------------")
	confirm_list_cursor = pymon.db.school.find({"_id": ObjectId(school_objid) })
	for record in confirm_list_cursor:
		print(record)
		print(record['accepted_students'])
	return return_bookmarks()



'''
Mongo find_by_id db.user.find({"_id" : ObjectId("573fdc635aeffc16e6ca6c83"}).pretty()
'''
