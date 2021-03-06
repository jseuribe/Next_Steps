from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired

#flask forms that are passed into an html file. Vestigial.
class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match.')])
	remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
	new_username = StringField('username', validators=[DataRequired()])
	new_email = StringField('email', validators=[DataRequired()])
	new_password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match.')])
