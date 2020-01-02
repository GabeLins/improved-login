from flask_login import login_user
from flask import Blueprint, render_template, redirect, request
from LoginSystem.models import User
from LoginSystem import db

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
            return print('Invalid username or password...') # TODO: Add endpoint

@auth.route('/register', methods=['POST', 'GET'])
def register ():
    if ( request.method == 'POST' ):
        first_name = request.form['first']
        last_name = request.form['last']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        email = request.form['email']

        username_error = User.query.filter_by(username=username).first()
        email_error = User.query.filter_by(email=email).first()
        match_error = password != confirm

        errors = [ username_error, email_error, match_error ]

        if ( not all(errors) ):
            user = User(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            db.session.add(user)
            db.session.commit()
            return print('SUCCESS!!') # TODO: Add endpoint
        
        # Error handlers
        if ( username_error ):
            return print('Username already in use...') # TODO: Add endpoint

        if ( email_error ):
            return print('Email already in use...') # TODO: Add endpoint

        if ( match_error ):
            return print('Passwords didn\'t match...') # TODO: Add endpoint
        