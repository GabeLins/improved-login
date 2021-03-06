from flask_login import UserMixin
from LoginSystem import db
import time


# User Database Model and Class
class User ( UserMixin, db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)


    def __init__ ( self, username, password, email, first_name, last_name ):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

        # TODO: Write a function to delete unverified users after a specific
        # time after its creation
        self.verified = False
        self.timestamp = int(time.time())
