import unicodedata
from app import app, db, pymon
from flask import g, request, url_for, render_template, flash, redirect, session
from .forms import LoginForm, RegisterForm
from flask.ext.login import current_user

def normalize_from_unicode(inp_str):
	unicode_vessel = unicodedata.normalize('NFKD', inp_str).encode('ascii', 'ignore')
	return unicode_vessel

def pull_random_schools():#Basic function that returns some schools.
	vessel = {}
	vessel = pymon.db.school.find().limit(-1).skip(413).next()
	return transform_to_School_obj(vessel)


def transform_to_School_obj(school_dict):
	from models import Schools
	new_school = Schools()
	new_school.instnm = normalize_from_unicode(school_dict[u'INSTNM'])
	new_school.city = normalize_from_unicode(school_dict[u'CITY'])
	return new_school
	