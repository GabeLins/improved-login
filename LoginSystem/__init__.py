from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'

import LoginSystem.views