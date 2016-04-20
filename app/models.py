import datetime
from flask import url_for
from app import db, lm
from bcrypt import hashpw, gensalt
from flask.ext.login import UserMixin
from utils import normalize_from_unicode

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

	#Eventually, we should add some other fields here (grades, other parameters, etc.)

'''
Here's where the school class goes
'''
