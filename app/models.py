import datetime
from flask import url_for
from app import db, lm
from bcrypt import hashpw, gensalt
from flask.ext.login import UserMixin
from utils import normalize_from_unicode

'''
School class used to retrieve School Documents from mongo
'''

class Schools(db.Document):
	id_num = db.StringField(max_length=255, required=False)
	actenmid = db.StringField(max_length=255, required=False)
	stabbr = db.StringField(max_length=255, required=False)
	adm_rate = db.FloatField(min_value=0, max_value=1.0)
	locale = db.IntField(min_value=0, max_value=255)
	numbranch = db.StringField(max_length=255, required=False)
	sat_avg = db.FloatField(min_value=0, required=False)
	actwr75 = db.FloatField(min_value=0, required=False)
	actcm25 = db.FloatField(min_value=0, required=False)
	ccsizset = db.FloatField(min_value=0, required=False)
	sat_avg_all = db.FloatField(min_value=0, required=False)
	opeid6 = db.FloatField(min_value=0, required=False)
	actwrmid = db.FloatField(min_value=0, required=False)
	control = db.FloatField(min_value=0, required=False)
	hcm2 = db.FloatField(min_value=0, required=False)
	preddeg = db.FloatField(min_value=0, required=False)
	adm_rate_all = db.FloatField(min_value=0, max_value=1.0, required=False)
	npcurl = db.StringField(max_length=255, required=False)
	satmtmid = db.FloatField(min_value=0, required=False)
	satmt75 = db.FloatField(min_value=0, required=False)
	instnm = db.StringField(max_length=255, required=False)
	satvr75 = db.FloatField(min_value=0, required=False)
	acten75 = db.FloatField(min_value=0, required=False)
	main = db.FloatField(min_value=0, required=False)
	insturl = db.StringField(max_length=255, required=False)
	actcm75 = db.FloatField(min_value=0, required=False)
	satvr25 = db.FloatField(min_value=0, required=False)
	actwr25 = db.FloatField(min_value=0, required=False)
	actmt75 = db.FloatField(min_value=0, required=False)
	actcmmid = db.FloatField(min_value=0, required=False)
	satmt25 = db.FloatField(min_value=0, required=False)
	satwr75 = db.FloatField(min_value=0, required=False)
	city = db.StringField(max_length=255, required=False)
	satvrmid = db.FloatField(min_value=0, required=False)
	ccbasic = db.FloatField(min_value=0, required=False)
	satwr25 = db.FloatField(min_value=0, required=False)
	accredAgency = db.StringField(min_value=255, required=False)
	region = db.FloatField(min_value=0, required=False)
	acten25 = db.FloatField(min_value=0, required=False)
	ccugprof = db.FloatField(min_value=0, required=False)
	bookmarks = db.IntField(min_value=0)
	accepted_student_ids = db.ListField(db.StringField(max_length=255))
	majors_list = db.ListField(db.IntField(min_value=0, max_value=39))

	meta = {#To declare admin users
		'allow_inheritance': True
	}

class User(db.Document):
	#Sign up Parameters. Created at registration
	user_id = db.IntField(min_value=0, max_value=9001)#this should be set by mongo to keep it incrementing and such
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	email = db.EmailField(max_length=255, required=True)
	username = db.StringField(max_length=255, required=True)
	#slug = db.StringField(max_length=255, required=True)#????
	hashed_pass = db.StringField(max_length=255, required=True)
	bookmarks =  db.ListField(db.ListField(db.StringField(max_length=255)))

	#name and address. Registration Page 1
	f_name = db.StringField(max_length=255, required=False)
	m_name = db.StringField(max_length=255, required=False)
	l_name = db.StringField(max_length=255, required=False)
	street = db.StringField(max_length=255, required=False)
	street_state = db.IntField(max_length=255, required=False)

	#Grades and Scores, major preference. Registration Page 2
	gpa = db.FloatField(min_value=0, max_value=100.0, required=False)
	ACT_Score = db.IntField(min_value=1, max_value=36, required=False)
	SAT_read = db.IntField(min_value=0,max_value=800, required=False)
	SAT_write = db.IntField(min_value=0,max_value=800, required=False)
	SAT_math = db.IntField(min_value=0,max_value=800, required=False)
	major_preference_list = db.ListField(db.StringField(max_length=255, required=False))

	#Tuition and Location. Registration Page 3
	tuition = db.FloatField(min_value=0, max_value=100000, required=False)
	state_preference_list = db.ListField(db.StringField(max_length=255, required=False))
	cost_preference = db.FloatField(min_value=0, max_value=5, required=False)
	distance_preference = db.FloatField(min_value=0, max_value=5, required=False)
	academic_preference = db.FloatField(min_value=0, max_value=5, required=False)	
	meta = {#To declare admin users
		'allow_inheritance': True
	}

	#Recommended Schools
	recommended_schools = db.DictField()

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.username)
		except NameError:
			return normalize_from_unicode(self.username)
