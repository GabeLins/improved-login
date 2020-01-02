from flask_login import login_user
from flask import Blueprint, render_template, redirect, request
from LoginSystem.models import User

auth = Blueprint('auth', __name__)

# Render functions
@auth.route('/login')
def render_login ():
    return render_template(
        'login.html',
        title='Sign in',
        script='/static/js/index.js'
    )

@auth.route('/register')
def render_register ():
    return render_template(
        'register.html',
        title='Sign up',
        script='/static/js/index.js'
    )


# Processing functions
@auth.route('/login', methods=['POST', 'GET'])
def login ():
    if ( request.method == 'POST' ):
        _user = request.form['user']
        _pass = request.form['pass']
        _keep = 'keep' in request.form

        user = User.query.filter_by(username=_user).first()
        if ( user and _pass == user.password ):
            return print('SUCCESS!!') # TODO: Add endpoint
        else:
            return print('ERROR!!') # TODO: Add endpoint

