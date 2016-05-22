import unicodedata
from app import app, db, pymon
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from flask.ext.login import current_user
from bson import ObjectId

def normalize_from_unicode(inp_str):
	unicode_vessel = unicodedata.normalize('NFKD', inp_str).encode('ascii', 'ignore')
	return unicode_vessel

def pull_random_schools():#Basic function that returns some schools.
	vessel = pymon.db.school.find({"INSTNM" : "Columbia University in the City of New York"})
	return transform_to_School_obj(vessel)


def transform_to_School_obj(cursor):
	from models import Schools
	print("in transform_to_School_obj")
	extracted_list = cursor[:]
	print("extracted", extracted_list)
	new_school = Schools()
	for record in extracted_list:
		print("Creating a response object")
		print('type in transform_to_School_obj')
		print(type(record))
		new_school.id_num = str(record[u'_id'])#obtain an object id for lookup purposes
		new_school.instnm = normalize_from_unicode(record[u'INSTNM'])
		new_school.city = normalize_from_unicode(record[u'CITY'])
		'''
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
		new_school.stabbr = normalize_from_unicode(record[u'STABBR'])
		new_school.sat_avg_all = float(normalize_from_unicode(record[u'SAT_AVG_ALL']))
		new_school.actenmid = normalize_from_unicode(record[u'ACTENMID'])
		new_school.adm_rate_all = float(normalize_from_unicode(record[u'ADM_RATE_ALL']))
		#new_school.avg_income = 
		#new_school.tuition = 
	return new_school

def find_school_by_name(s_name):#Debugging purposes?
	print(s_name)
	u_s_name = unicode(s_name, "utf-8")
	school_cursor = pymon.db.school.find({"INSTNM" : u_s_name})
	query_count = school_cursor.count()
	print("the count: ", query_count)
	if query_count == 0:
		print("No school found...")
	else:
		print("School found!")
	return transform_to_School_obj(school_cursor)

def resolve_school_objid(school_obj_id):
	from models import Schools
	print("Find school by id")
	print(school_obj_id)
	cursor_list = pymon.db.school.find({"_id": ObjectId(school_obj_id) })
	new_school = Schools()
	for record in cursor_list:
		print("A school has been found")
		new_school.id_num = str(record[u'_id'])#obtain an object id for lookup purposes
		new_school.instnm = normalize_from_unicode(record[u'INSTNM'])
		new_school.city = normalize_from_unicode(record[u'CITY'])
		'''
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
		new_school.stabbr = normalize_from_unicode(record[u'STABBR'])
		new_school.sat_avg_all = float(normalize_from_unicode(record[u'SAT_AVG_ALL']))
		new_school.actenmid = normalize_from_unicode(record[u'ACTENMID'])
		new_school.adm_rate_all = float(normalize_from_unicode(record[u'ADM_RATE_ALL']))
		#new_school.avg_income = 
		#new_school.tuition = 
	return new_school


	