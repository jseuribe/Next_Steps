from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired

class LoginForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match.')])
	remember_me = BooleanField('remember_me', default=False)