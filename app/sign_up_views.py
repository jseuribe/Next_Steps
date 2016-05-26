from app import app
from flask import g, request, url_for, render_template, flash, redirect, session
from views import login_required, return_account_setup, return_account_setup_2, return_account_setup_3, return_account_setup_4, return_log
from utils import normalize_from_unicode
from models import User
from auth import *
'''
PURPOSE: functions that handle user setup and registration.
'''

'''
If the html page that uses the action "account_setup"
calls this method with the form:

<form action='/account_setup' method='POST'>
	<label for ='FIELD1'>FIELD1: </label>
	<input type='text' name='FIELD1" /> <br />
	<input type='submit'/>
</form>

Then your method should look like:

@app.route('/account_setup', methods=['POST'])
def account_setup():
	FIELD1 = request.form['FIELD1'] #Should obtain FIELD1
'''


'''
account_setup_0 handles input from the account_setup_0 page.
'''
@app.route('/')
@app.route('/account_setup_0/confirm', methods=['POST'])
def account_setup_0():
	session['completion'] = '1' #puts a cookie in that denotes that the user is up to the following step
	print("Registration Time")
	if 'user_id' in session:
		flash('You are logged in already!')
		return return_account_setup_1()
	else:
		#obtain data from the html form request
		n_username = normalize_from_unicode(request.form['Email'])
		n_email = normalize_from_unicode(request.form['Email'])
		n_passw = normalize_from_unicode(request.form['Password'])
		n_v_passw = normalize_from_unicode(request.form['Repassword'])
		existing_user = User.objects(username=n_username)

		#verify that the email is not used in the DB
		if existing_user:
			flash('Username not available!')
			return redirect(url_for('return_log'))

		#Verifies password and login info
		if not n_username and not n_email and not n_passw and not n_v_passw:
			print('Checks have failed')
			flash("error, please do not leave any field blank")
			return return_account_setup()
		elif n_passw != n_v_passw:
			print('Mismatching passwords')
			flash("Passwords do not match, re-enter both")
			return return_account_setup()
		else:
			print('all checks made, creating a new user')
			#Create and save the user to the DB
			new_user = User()
			new_user.email = n_email
			new_user.username = n_username
			new_user.hashed_pass = hashpw(n_passw, gensalt())
			new_user.progress_setup = False
			new_user.save()
			does_user_exist_now = User.objects(username=n_username)

			if not does_user_exist_now:
				print('user was not found')
				flash('Something went wrong; please try again.')
				return return_account_setup()
			else:#The object is correct!
				print(does_user_exist_now[0].email)
				unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
				retrieved_name = unicode_vessel
				login_user(new_user, remember='no')
				print('new user is logged in')
				flash("Logged in for the first time!, category='success'")
	#save some cookie info
	session['logged_in'] = True
	session['username'] = n_email
	session['completion'] = '1'
	print("Registration is a success")
	return return_account_setup_1()

'''
Simple render template function that returns account_setup_1
'''
@app.route('/')
@app.route('/account_setup_1', methods=['GET'])
@login_required
def return_account_setup_1():
	return render_template('/Web_Development/account_setup_1.html', title='Account Setup (Step 2 of 4)')

'''
account_setup_1()
This handles requests from account_setup_1
'''
@app.route('/')
@app.route('/account_setup_1/confirm', methods=['POST'])
@login_required
def account_setup_1():
	#obtain data from request
	n_f_name = normalize_from_unicode(request.form['First'])
	n_m_name = normalize_from_unicode(request.form['Middle'])
	n_l_name = normalize_from_unicode(request.form['Last'])
	n_street = normalize_from_unicode(request.form['Street'])
	n_state = int(normalize_from_unicode(request.form['state']))


	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_q = User.objects(username=u_name_look_up) #get the object

	#verify the user is in the db
	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_1'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.f_name = n_f_name
	user_obj.m_name = n_m_name
	user_obj.l_name = n_l_name
	user_obj.street = n_street
	user_obj.street_state = n_state
	#Save the object and update the cookies
	user_obj.save()
	session['completion'] = '2'

	return return_account_setup_2()

'''
account_setup_2() handles input from the page of the same name
'''
@app.route('/')
@app.route('/account_setup_2/confirm', methods=['POST'])
@login_required
def account_setup_2():
	#obtain data
	n_gpa = float(normalize_from_unicode(request.form['gpa']))
	n_read = int(normalize_from_unicode(request.form['Read']))
	n_math = int(normalize_from_unicode(request.form['Math']))
	n_write = int(normalize_from_unicode(request.form['Write']))
	n_degree = normalize_from_unicode(request.form['degree'])
	n_act_english = 1
	n_act_writing = 1
	n_act_math = 1
	if request.form['ACT_English']:
		n_act_english = int(normalize_from_unicode(request.form['ACT_English']))
	if request.form['ACT_Reading']:
		n_act_writing = int(normalize_from_unicode(request.form['ACT_Reading']))
	if request.form['ACT_Math']:
		n_act_math = int(normalize_from_unicode(request.form['ACT_Math']))


	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.
	major_list = request.form.getlist('majors')
	user_q = User.objects(username=u_name_look_up) #get the object

	#verify data is good
	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_1'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.gpa = n_gpa
	user_obj.SAT_read = n_read
	user_obj.SAT_math = n_math
	user_obj.SAT_write = n_write
	user_obj.pref_degree = n_degree
	user_obj.major_preference_list = major_list
	user_obj.ACT_English = n_act_english
	user_obj.ACT_Reading = n_act_writing
	user_obj.ACT_Math = n_act_math
	#save and update cookie
	user_obj.save()
	session['completion'] = '3'
	return redirect(url_for('return_account_setup_3'))

'''
account_setup_3 handles input from the page of the same name
'''
@app.route('/')
@app.route('/account_setup_3/confirm', methods=['POST'])
@login_required
def account_setup_3():
	#obtain data from the request
	n_tuition = float(normalize_from_unicode(request.form['tuition']))
	n_distance_preference = float(normalize_from_unicode(request.form['distance_preference']))
	n_academic_preference = float(normalize_from_unicode(request.form['academic_preference']))
	n_cost_preference = float(normalize_from_unicode(request.form['cost_preference']))
	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.
	form_state_list = request.form.getlist('state_list')

	user_q = User.objects(username=u_name_look_up) #get the object

	#Verify the user is existing
	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_3'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.tuition = n_tuition
	user_obj.distance_preference = n_distance_preference
	user_obj.academic_preference = n_academic_preference
	user_obj.cost_preference = n_cost_preference
	user_obj.state_preference_list = form_state_list
	user_obj.progress_setup = True#Marks in the DB that the user has completed the setup phase
	#Save the data and the cookie updates
	user_obj.save()
	session['completion'] = 'complete'
	return return_account_setup_4()

