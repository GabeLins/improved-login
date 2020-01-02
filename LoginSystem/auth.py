from flask import Blueprint, render_template, redirect
from flask_login import login_user, login_required
from flask_login import logout_user, current_user
from bcrypt import hashpw, checkpw, gensalt
from flask import request, flash, url_for
from LoginSystem.models import User
from LoginSystem import db

auth = Blueprint('auth', __name__)
errs = {}


# Render functions
@auth.route('/login')
def render_login ():
    global errs
    errors = errs
    errs = { 'user':'', 'pass':'', 'leng':'', 'mail':'',
             'logn':'', 'name':'', 'last':'' }
             
    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'login.html',
        title='Sign in',
        errors=errors
    )


@auth.route('/register')
def render_register ():
    global errs
    errors = errs
    errs = { 'user':'', 'pass':'', 'leng':'', 'mail':'',
             'logn':'', 'name':'', 'last':'' }

    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'register.html',
        title='Sign up',
        errors=errors
    )



# Processing functions
@auth.route('/login', methods=['POST', 'GET'])
def login ():
    global errs

    if ( request.method == 'POST' ):
        _user = request.form['user']
        _pass = request.form['pass']
        _keep = 'keep' in request.form

        user = User.query.filter_by(username=_user).first()
        if ( user and checkpw(bytes(_pass, 'utf-8'), user.password)):
            login_user(user, remember=_keep)
            return redirect(url_for('home'))
        else:
            errs['logn'] = 'Invalid username or password.'
            return redirect(url_for('auth.login'))


@auth.route('/register', methods=['POST', 'GET'])
def register ():
    global errs

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
                password=hashpw(bytes(password, 'utf-8'), gensalt()),
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
