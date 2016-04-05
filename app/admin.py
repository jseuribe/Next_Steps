from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from app.auth import requires_auth
from app.models import Post, Comment

admin = Blueprint('admin', __name__, template_folder='templates')