from app import app
from flask import g, request, url_for, render_template, flash, redirect, session
from views import login_required, return_account_setup, return_account_setup_2, return_account_setup_3, return_account_setup_4
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
@app.route('/register_n', methods=['POST'])
def register_n():
	#Obtain some initial information from the request form

	password = normalize_from_unicode(request.form['Password'])
	verify_password = normalize_from_unicode(request.form['Repassword'])

	email = normalize_from_unicode(request.form['Email'])

	#f_name = normalize_from_unicode(request.form['f_name'])
	#l_name = normalize_from_unicode(request.form['l_name'])
	
	#Other fields will probably be squeezed in here. Or perhaps in another function?

	#include a check for if password == verify_password
	if not password and not verify_password and not email:
		print("CRITICAL ERROR")
	else:
		#normal execution
		#Initialize the basic profile info to this other information
		new_user = User()
		new_user.username = email #Are user-names required?
		new_user.email = email
		new_user.hashed_pass = hashpw(password, gensalt())
		new_user.save()#Save the user after populating it with the new information

		does_user_exist_now = User.objects(username=normalized_name)
		retrieved_name = ''
		if not does_user_exist_now:#Not sure when this could happen. But good to check otherwise
			print("CATASTROPHIC ERROR")
			return redirect('{{url_for("account_setup.html")}}')
		else:#The object is correct! Now create a new context and log the new user in
			unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
			retrieved_name = unicode_vessel
			login_user(new_user, remember='no')
			flash("Logged in for the first time!", category='success')

	return render_template('\Web_Development\account_setup_1.html')


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

		#print("the input: ", n_username, n_)
		if not n_username and not n_email and not n_passw and not n_v_passw:
			flash("error, please do not leave any field blank")
			return return_account_setup()
		elif n_passw != n_v_passw:
			flash("Passwords do not match, re-enter both")
			return return_account_setup()
		else:
			new_user = User()
			new_user.email = n_email
			new_user.username = n_username#Not sure if we'll implement a separate username. this should suffice for now, though
			new_user.hashed_pass = hashpw(n_passw, gensalt())
			new_user.save()
			does_user_exist_now = User.objects(username=n_username)
			if not does_user_exist_now:
				flash('Something went wrong; please try again.')
				return return_account_setup()
			else:#The object is correct!
				unicode_vessel = normalize_from_unicode(does_user_exist_now[0].username)
				retrieved_name = unicode_vessel
				login_user(new_user, remember='no')
				flash("Logged in for the first time!, category='success'")
	session['logged_in'] = True
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

	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_q = User.objects(username=u_name_look_up) #get the object

	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_1'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.gpa = n_gpa
	user_obj.SAT_read = n_read
	user_obj.SAT_math = n_math
	user_obj.SAT_write = n_write
	user_obj.degree = n_degree
	user_obj.save()
	return redirect(url_for('return_account_setup_3'))

@app.route('/')
@app.route('/account_setup_3/confirm', methods=['POST'])
@login_required
def account_setup_3():
	n_tuition = float(normalize_from_unicode(request.form['tuition']))
	n_dorm_price = float(normalize_from_unicode(request.form['dorm_price']))
	n_state = normalize_from_unicode(request.form['state'])
	n_distance_preference = float(normalize_from_unicode(request.form['distance_preference']))
	n_academic_preference = float(normalize_from_unicode(request.form['academic_preference']))
	n_cost_preference = float(normalize_from_unicode(request.form['cost_preference']))
	u_name_look_up = normalize_from_unicode(session['user_id'])#Retrieve user_name to load from db.

	user_q = User.objects(username=u_name_look_up) #get the object

	if not user_q:
		flash("Error please try again - USER_NOT_FOUND")
		return redirect(url_for('return_account_setup_3'))

	user_obj = user_q[0]#This should be the object what is the user.
	user_obj.tuition = n_tuition
	user_obj.dorm_price = n_dorm_price
	user_obj.state = n_state
	user_obj.distance_preference = n_distance_preference
	user_obj.academic_preference = n_academic_preference
	user_obj.cost_preference = n_cost_preference
	user_obj.save()
	return return_account_setup_4()

