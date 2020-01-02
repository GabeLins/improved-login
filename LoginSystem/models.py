from flask_login import UserMixin
from LoginSystem import db

class User ( UserMixin, db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __init__ ( self, username, password, email ):
        self.username = username
        self.password = password
        self.email = email
