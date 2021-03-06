from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
import bcrypt
import pymongo

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0')

lm = LoginManager()
lm.init_app(app)

app.config.from_object('config')
app.config["MONGODB_SETTINGS"] = {'DB': "nextsteps"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config['MONGO_DBNAME'] = "nextsteps"
db = MongoEngine(app)
pymon = PyMongo(app)
from app import views

#Flask LoginManager allows you to easily store "login" context
#It also lets you login/logout.
#This also allows users to restrict views to logged-in or logged out users






