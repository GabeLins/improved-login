from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
import json

# Load the settings JSON file
with open('settings.json', 'r') as setup_file:
    settings = json.load(setup_file)

# Create the Flask app
app = Flask(__name__)

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = settings['secret_key']

# Create the app database
db = SQLAlchemy()
db.init_app(app)

# Create the app Login Manager
login_mgr = LoginManager(app)
login_mgr.login_view = 'auth.login'
login_mgr.init_app(app)

# Load database models and auth blueprint
from LoginSystem.models import User
from LoginSystem.auth import auth
@login_mgr.user_loader
def load_user ( user_id ):
    user = User.query.get(user_id)
    return user

# Register auth blueprint
app.register_blueprint(auth)

import LoginSystem.views
