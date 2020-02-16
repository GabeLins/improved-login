# Flask modules
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

# Login manager
login_mgr = LoginManager(app)
login_mgr.login_view = 'auth.login'
login_mgr.init_app(app)

# User loader
from LoginSystem.models import User
from LoginSystem.auth import auth
@login_mgr.user_loader
def load_user ( user_id ):
    user = User.query.get(user_id)
    return user

# App blueprints
app.register_blueprint(auth)

import LoginSystem.views
