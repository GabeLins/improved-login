from flask import Blueprint, render_template, redirect, \
    request, flash, url_for
from flask_login import login_user, login_required, \
    logout_user, current_user
from LoginSystem.models import User
from LoginSystem import db
import hashlib

auth = Blueprint('auth', __name__)
errs = {}


def encrypt ( string ):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


# Render functions
@auth.route('/login')
def render_login ():
    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'login.html',
        title='Sign in',
        script='/static/js/index.js'
    )


@auth.route('/register')
def render_register ():
    global errs
    errors = errs
    errs = { 'user':'', 'pass':'', 'leng':'', 'mail':'' }

    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'register.html',
        title='Sign up',
        script='/static/js/index.js',
        errors=errors
    )



# Processing functions
@auth.route('/login', methods=['POST', 'GET'])
def login ():
    if ( request.method == 'POST' ):
        _user = request.form['user']
        _pass = request.form['pass']
        _keep = 'keep' in request.form

        user = User.query.filter_by(username=_user).first()
        if ( user and encrypt(_pass) == user.password ):
            login_user(user, remember=_keep)
            return redirect(url_for('home'))
        else:
            return print('Invalid username or password...') # TODO: Add flash


@auth.route('/register', methods=['POST', 'GET'])
def register ():
    global errs
    errs = { 'user':'', 'pass':'', 'leng':'', 'mail':'' }

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
        length_error = len(password) < 8
        lname_error = last_name == ''
        fname_error = first_name == ''

        errors = [ username_error, email_error, match_error, 
                   length_error, lname_error, fname_error ]

        if ( not any(errors) ):
            user = User(
                username=username,
                password=encrypt(password),
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        # Error handlers
        if ( fname_error ):
            errs['name'] = 'Empty field.'

        if ( lname_error ):
            errs['last'] = 'Empty field.'

        if ( username_error ):
            errs['user'] = 'Username already in use.'

        if ( email_error ):
            errs['mail'] = 'Email already in use.'
        
        if ( length_error ):
            errs['leng'] = 'Password must be at least 8 characters long.'

        elif ( match_error ):
            errs['pass'] = 'Passwords didn\'t match.'

        return redirect(url_for('auth.register'))


@auth.route('/logout')
@login_required
def logout ():
    logout_user()
    return redirect(url_for('auth.login'))
