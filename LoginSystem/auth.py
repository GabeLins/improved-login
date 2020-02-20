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

        errs['user'] = '' if not User.query.filter_by(username=username).first() else 'Username already in use.'
        errs['mail'] = '' if not User.query.filter_by(email=email).first() else 'Email already in use.'
        errs['pass'] = '' if password == confirm else 'Passwords didn\'t match.'
        errs['leng'] = '' if len(password) >= 8 else 'Password must be at least 8 characters long.'
        errs['last'] = '' if last_name else 'Empty field.'
        errs['name'] = '' if first_name else 'Empty field.'

        if ( not any(errs.values()) ):
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

        return redirect(url_for('auth.register'))


@auth.route('/logout')
@login_required
def logout ():
    logout_user()
    return redirect(url_for('auth.login'))
