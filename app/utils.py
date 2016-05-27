import unicodedata
from app import app, db, pymon
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from flask.ext.login import current_user
from bson import ObjectId
import json
import requests

'''
PURPOSE: A robust number of helper functions used throughout the views files
'''

'''
Verifies if a school has been bookmarked already, in order to prevent users from bookmarking a school twice

'''

def gen_img_url(lati_param, longi_param):
	# Get the url of a location search based on latitude and longitude.
	lati = str(lati_param)
	longi = str(longi_param)
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lati + "," + longi + "&radius=300&keyword=university&key=AIzaSyCqenz7cYYbtekGNOthV0jm7ROx7NJKThc"
	# Get the JSON data
	json_data = (json.loads(requests.get(url).text))
	# Default Picture
	photo_url = "http://andrewprokos.com/d/new-york-skyline-world-trade-center-night?g2_itemId=25228"
	# If there are zero results, photo_url will be default picture.
	# If there are results, photo_url will be school picture.
	if 'status' in json_data:
	    if json_data['status'] != "ZERO_RESULTS":
	        if 'results' in json_data:
	            if 'photos' in json_data['results'][0]:
	                if 'photo_reference' in json_data['results'][0]['photos'][0]:
	                    photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&photoreference=" + json_data['results'][0]['photos'][0]['photo_reference'] + "&key=AIzaSyCqenz7cYYbtekGNOthV0jm7ROx7NJKThc"
	return photo_url

def isbookmarked(string_objid, bookmark_list):
	norm_test_objid = normalize_from_unicode(string_objid)
	for item in bookmark_list:
		current_objid = item[0]#Get the current bookmark
		norm_item_objid = normalize_from_unicode(current_objid)
		if norm_item_objid == norm_test_objid:
			print("in your bookmarks")
			return True
		elif not norm_test_objid is norm_item_objid:
			print("Not in your bookmarks")
			continue
	return False

'''
Transforms unicode object to str
Strips away awful unicode from an otherwise beautiful string.
'''
def normalize_from_unicode(inp_str):
	unicode_vessel = unicodedata.normalize('NFKD', inp_str).encode('ascii', 'ignore')
	return unicode_vessel

def pull_random_schools():#Basic function that returns some schools.
	vessel = pymon.db.school.find({"INSTNM" : "Columbia University in the City of New York"})
	return transform_to_School_obj(vessel)


'''
transform_to_School_obj(mongoDBCursor, name, fit_number)

Looks up in the DB the school by name, and returns a schools object that contains important school data.
'''
def transform_to_School_obj(cursor, s_name, fit):
	from models import Schools#python is weird
	print("in transform_to_School_obj")
	#print(fit_list[u'CUNY Hunter College'])
	extracted_list = cursor[:]
	print("extracted", extracted_list)
	new_school = Schools()
	print("FIT NUMBER IS!!!!!!!!!")
	print(fit)
	for record in extracted_list:
		print("Creating a response object")
		print('type in transform_to_School_obj')
		print(type(record))
		new_school.id_num = str(record[u'_id'])#obtain an object id for lookup purposes
		new_school.instnm = normalize_from_unicode(record[u'INSTNM'])
		new_school.city = normalize_from_unicode(record[u'CITY'])
		'''
		reference
								<p class="lead">Website: </p>
								<p class="lead">Address: </p>
								<p class="lead">State: </p>
								<hr>
								<p class="lead">SAT Average: </p>
								<p class="lead">ACT Average: </p>
								<p class="lead">Admission Rate: </p>
								<p class="lead">Average Income of Student: </p>
								<p class="lead">Tuition: </p>
		'''
		new_school.insturl = normalize_from_unicode(record[u'INSTURL'])
		if record[u'STABBR'] == u'NULL':
			new_school.stabbr = "NULL"
		else:
			new_school.stabbr = normalize_from_unicode(record[u'STABBR'])
		if record[u'SAT_AVG_ALL'] == u'NULL':
			new_school.sat_avg_all = 0
		else:
			new_school.sat_avg_all = float(normalize_from_unicode(record[u'SAT_AVG_ALL']))
		if record[u'ACTENMID'] == u'NULL':
			new_school.actenmid = 0
		else:
			new_school.actenmid = normalize_from_unicode(record[u'ACTENMID'])
		if record[u'ADM_RATE_ALL'] == u'NULL':
			new_school.adm_rate_all = 0
		else:
			new_school.adm_rate_all = float(normalize_from_unicode(record[u'ADM_RATE_ALL']))
		new_school.longi = float(normalize_from_unicode(record[u'LONGITUDE']))
		new_school.lati = float(normalize_from_unicode(record[u'LATITUDE']))
		new_school.fit_number = fit
		new_school.school_img_url = gen_img_url(new_school.lati, new_school.longi)
	return new_school

'''
Finds a school by name, and returns a school object
'''
def find_school_by_name(s_name, fit_list):#Debugging purposes?
	print(s_name)
	school_cursor = pymon.db.school.find({"INSTNM" : s_name})#pymongo query
	query_count = school_cursor.count()
	print("the count: ", query_count)
	if query_count == 0:
		print("No school found...")
	else:
		print("School found!")
	return transform_to_School_obj(school_cursor, s_name, fit_list[s_name])

'''
finds a school by object_id, and returns a Schools object
'''
def resolve_school_objid(school_obj_id):
	from models import Schools#Python is weird

	print("Find school by id")
	print(school_obj_id)
	cursor_list = pymon.db.school.find({"_id": ObjectId(school_obj_id) })
	query_result = cursor_list.count()
	if query_result == 0:
		print("Error! No school")
		return None
	new_school = Schools()
	for record in cursor_list:
		print("A school has been found")
		new_school.id_num = str(record[u'_id'])#obtain an object id for lookup purposes
		new_school.instnm = normalize_from_unicode(record[u'INSTNM'])
		new_school.city = normalize_from_unicode(record[u'CITY'])
		'''
		HTML Reference
								<p class="lead">Website: </p>
								<p class="lead">Address: </p>
								<p class="lead">State: </p>
								<hr>
								<p class="lead">SAT Average: </p>
								<p class="lead">ACT Average: </p>
								<p class="lead">Admission Rate: </p>
								<p class="lead">Average Income of Student: </p>
								<p class="lead">Tuition: </p>
		'''
		#Additional information that can be displayed
		new_school.insturl = normalize_from_unicode(record[u'INSTURL'])
		if record[u'STABBR'] == u'NULL':
			new_school.stabbr = "NULL"
		else:
			new_school.stabbr = normalize_from_unicode(record[u'STABBR'])
		if record[u'SAT_AVG_ALL'] == u'NULL':
			new_school.sat_avg_all = 0
		else:
			new_school.sat_avg_all = float(normalize_from_unicode(record[u'SAT_AVG_ALL']))
		if record[u'ACTENMID'] == u'NULL':
			new_school.actenmid = 0
		else:
			new_school.actenmid = normalize_from_unicode(record[u'ACTENMID'])
		if record[u'ADM_RATE_ALL'] == u'NULL':
			new_school.adm_rate_all = 0
		else:
			new_school.adm_rate_all = float(normalize_from_unicode(record[u'ADM_RATE_ALL']))
	return new_school

'''
simple function that extracts school objects from a user's bookmark list
'''
def extract_bookmarks(school_id_list):
	school_objects = []
	for item in school_id_list:
		current_school = resolve_school_objid(item[0])#Find by the bookmark's ID.
		if not current_school:
			continue
		else:
			school_objects.append(current_school)

	return school_objects

'''
checks if the user has completed setup.
'''
def setup_complete(username):
	setup_val = False
	user_string_name = username
	user_cursor = pymon.db.user.find({"username" : user_string_name})
	query_count = user_cursor.count()
	print("the count: ", query_count)
	if query_count == 0:
		print("No User found...")
		return False
	else:
		for record in user_cursor:
			setup_val = record['progress_setup']
			return setup_val

	return setup_val


