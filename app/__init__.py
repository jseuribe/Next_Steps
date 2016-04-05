from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
import bcrypt
app = Flask(__name__)
app.config.from_object('config')
app.config["MONGODB_SETTINGS"] = {'DB': "nextsteps"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)
from app import views

lm = LoginManager()
lm.init_app(app)
if __name__ == '__main__':
	app.run()