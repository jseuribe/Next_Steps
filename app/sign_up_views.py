from app import app
from flask import g, request, url_for, render_template, flash, redirect, session
from views import login_required, return_account_setup, return_account_setup_2, return_account_setup_3, return_account_setup_4, return_log
from utils import normalize_from_unicode
from models import User
from auth import *
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

"""
function register() handles registration once called from the appropriate action form in
account_setup.html.

Currently this expects only 5 fields (password & pass verification, email, first and last names)
This can be easily expanded to receive other input as we see fit, or it can be separated into other fields
"""

@app.route('/')
@app.route('/account_setup_0/confirm', methods=['POST'])
def account_setup_0():

	print("Registration Time")
	if 'user_id' in session:
		flash('You are logged in already!')
		return return_account_setup_1()
	else:
		n_username = normalize_from_unicode(request.form['Email'])
		n_email = normalize_from_unicode(request.form['Email'])
		n_passw = normalize_from_unicode(request.form['Password'])
		n_v_passw = normalize_from_unicode(request.form['Repassword'])
		existing_user = User.objects(username=n_username)
		if existing_user:
			flash('Username not available!')
			return redirect(url_for('return_log'))

		#print("the input: ", n_username, n_)
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
			new_user = User()
			new_user.email = n_email
			new_user.username = n_username#Not sure if we'll implement a separate username. this should suffice for now, though
			new_user.hashed_pass = hashpw(n_passw, gensalt())
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
	session['logged_in'] = True
	session['username'] = n_email
	print("Registration is a success")
	return return_account_setup_1()

@app.route('/')
@app.route('/account_setup_1', methods=['GET'])
@login_required
def return_account_setup_1():
	return render_template('/Web_Development/account_setup_1.html', title='Account Setup (Step 2 of 4)')

@app.route('/')
@app.route('/account_setup_1/confirm', methods=['POST'])
@login_required
def account_setup_1():
	n_f_name = normalize_from_unicode(request.form['First'])
	n_m_name = normalize_from_unicode(request.form['Middle'])
	n_l_name = normalize_from_unicode(request.form['Last'])
	n_street = normalize_from_unicode(request.form['Street'])
	n_state = int(normalize_from_unicode(request.form['state']))


	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_q = User.objects(username=u_name_look_up) #get the object

	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_1'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.f_name = n_f_name
	user_obj.m_name = n_m_name
	user_obj.l_name = n_l_name
	user_obj.street = n_street
	user_obj.street_state = n_state
	user_obj.save()
	return return_account_setup_2()

@app.route('/')
@app.route('/account_setup_2/confirm', methods=['POST'])
@login_required
def account_setup_2():
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
	user_obj.save()
	return redirect(url_for('return_account_setup_3'))

@app.route('/')
@app.route('/account_setup_3/confirm', methods=['POST'])
@login_required
def account_setup_3():
	n_tuition = float(normalize_from_unicode(request.form['tuition']))
	n_distance_preference = float(normalize_from_unicode(request.form['distance_preference']))
	n_academic_preference = float(normalize_from_unicode(request.form['academic_preference']))
	n_cost_preference = float(normalize_from_unicode(request.form['cost_preference']))
	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.
	form_state_list = request.form.getlist('state_list')

	user_q = User.objects(username=u_name_look_up) #get the object

	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_3'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.tuition = n_tuition
	user_obj.distance_preference = n_distance_preference
	user_obj.academic_preference = n_academic_preference
	user_obj.cost_preference = n_cost_preference
	user_obj.state_preference_list = form_state_list
	user_obj.save()
	return return_account_setup_4()

