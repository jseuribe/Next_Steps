import datetime
from flask import url_for
from app import db, lm
from bcrypt import hashpw, gensalt
from flask.ext.login import UserMixin
from utils import normalize_from_unicode
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

'''
class Comment(db.EmbeddedDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	body = db.StringField(verbose_name="Comment", required=True)
	author = db.StringField(verbose_name="Name", max_length=255, required=True)
	
class Post(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required= True)
	title = db.StringField(max_length=255, required=True)
	slug = db.StringField(max_length=255, required=True)
	body = db.StringField(required=True)
	comments = db.ListField(db.EmbeddedDocumentField('Comment'))

	def get_absolute_url(self):
		return url_for('post', kwargs={"slug": self.slug})

	def __unicode__(self):
		return self.title

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}
'''

class User(db.Document):
	user_id = db.IntField(min_value=0, max_value=9001)#this should be set by mongo to keep it incrementing and such
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	email = db.EmailField(max_length=255, required=True)
	username = db.StringField(max_length=255, required=True)
	#slug = db.StringField(max_length=255, required=True)#????
	hashed_pass = db.StringField(max_length=255, required=True)

	#name and address
	f_name = db.StringField(max_length=255, required=False)
	m_name = db.StringField(max_length=255, required=False)
	l_name = db.StringField(max_length=255, required=False)
	street = db.StringField(max_length=255, required=False)

	gpa = db.FloatField(min_value=0, max_value=4.0, required=False)
	SAT_read = db.IntField(min_value=0,max_value=800, required=False)
	SAT_write = db.IntField(min_value=0,max_value=800, required=False)
	SAT_math = db.IntField(min_value=0,max_value=800, required=False)
	degree = db.StringField(max_length=255, required=False)
	meta = {#To declare admin users
		'allow_inheritance': True
	}

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

	'''
	def generate_auth_token(self, expiration = 600):
		s = Serializer(app.config["SECRET_KEY"], expires_in = expiration)
		return s.dumps({'id': self.username})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None #valid token that has expired
		except BadSignature:
			return None #invalid token
		user = User.query.get
	#Eventually, we should add some other fields here (grades, other parameters, etc.)
	'''

'''
Here's where the school class goes
'''
