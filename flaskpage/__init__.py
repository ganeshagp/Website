from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
                

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mongodb+srv://digitransservices:<ZC8YzvyMLpTyOfI2>@cluster0.tzxrmgb.mongodb.net/?retryWrites=true&w=majority'
db = SQLAlchemy(app) 
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

login_manager.login_view='login'
login_manager.login_message_category='info'

with app.app_context():
    db.init_app(app)
    db.create_all()

from flaskpage import routes
