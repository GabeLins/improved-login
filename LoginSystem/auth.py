from flask import Blueprint, render_template, redirect, abort
from flask_login import login_user, login_required
from flask_login import logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from bcrypt import hashpw, checkpw, gensalt
from flask import request, flash, url_for
from LoginSystem import db, settings
from LoginSystem.models import User
from LoginSystem.email import *


serializer = URLSafeTimedSerializer(settings['secret_key'])
auth = Blueprint('auth', __name__)
errs = {}

# Render functions
@auth.route('/login')
def render_login ():
    errors = dict(errs)
    errs.clear()
             
    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'login.html',
        title='Sign in',
        errors=errors,
        style='login.css'
    )


@auth.route('/register')
def render_register ():
    errors = dict(errs)
    errs.clear()

    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'register.html',
        title='Sign up',
        errors=errors,
        style='register.css'
    )


@auth.route('/recover')
def render_recover ():
    errors = dict(errs)
    errs.clear()

    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'recover.html',
        title='Recover Account',
        errors=errors
    )



# Processing functions
@auth.route('/login', methods=['POST', 'GET'])
def login ():
    if ( request.method == 'POST' ):
        _mail = request.form['email']
        _pass = request.form['password']
        _keep = 'keep' in request.form

        user = User.query.filter_by(email=_mail).first()
        if ( not user.verified ):
            errs['vrfy'] = 'Please, verify your email.'
            return redirect(url_for('auth.login'))
        
        if ( user and checkpw(bytes(_pass, 'utf-8'), user.password)):
            login_user(user, remember=_keep)
            return redirect(url_for('home'))
        
        else:
            errs['logn'] = 'Invalid email or password.'
            return redirect(url_for('auth.login'))



@auth.route('/register', methods=['POST', 'GET'])
def register ():
    if ( request.method == 'POST' ):
        first_name = request.form['first']
        last_name = request.form['last']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        email = request.form['email']
        agree = 'agree' in request.form

        if ( not agree ):
            errs['term'] = 'You need to agree to our terms to create an account.'
            return redirect(url_for('auth.register'))

        errs['user'] = (
            ''
            if not User.query.filter_by(username=username).first()
            else 'Username already in use.'
        )
        errs['mail'] = (
            ''
            if not User.query.filter_by(email=email).first()
            else 'Email already in use.'
        )
        errs['leng'] = (
            ''
            if len(password) >= 8
            else 'Password must be at least 8 characters long.'
        )
        errs['pass'] = '' if password == confirm else "Passwords didn't match."
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
            ticket = serializer.dumps(email, salt='verify-account')
            send_mail(
                (request.url_root, request.headers['Host']), 
                ticket, email, 'verify'
            )
            return redirect(url_for('auth.login'))

        return redirect(url_for('auth.register'))


@auth.route('/verify/<ticket>', methods=['POST', 'GET'])
def verify ( ticket ):
    try:
        email = serializer.loads(ticket, salt='verify-account', max_age=86400)
    except:
        return abort(401)

    if ( request.method == 'GET' ):
        user = User.query.filter_by(email=email).first()
        user.verified = True
        db.session.commit()

        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout ():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/recover', methods=['POST', 'GET'])
def recover ():
    if ( request.method == 'POST' ):
        email = request.form['mail']

        errs['recv'] = (
            ''
            if User.query.filter_by(email=email).first()
            else 'Invalid email address.'
        )

        if ( errs['recv'] ):
            return redirect(url_for('auth.recover'))
        
        ticket = serializer.dumps(email, salt='reset-password')
        send_mail(
            (request.url_root, request.headers['Host']), 
            ticket, email, 'reset'
        )

    return redirect(url_for('auth.login'))


@auth.route('/reset/<ticket>', methods=['POST', 'GET'])
def reset ( ticket ):
    errors = dict(errs)
    errs.clear()

    try:
        email = serializer.loads(ticket, salt='reset-password', max_age=300)
    except:
        return abort(401)

    if ( request.method == 'GET' ):
        return render_template(
            'reset.html',
            title=email,
            errors=errors
        )

    if ( request.method == 'POST' ):
        password = request.form['password']
        confirm = request.form['confirm']

        errs['leng'] = (
            ''
            if len(password) >= 8
            else 'Password must be at least 8 characters long.'
        )
        errs['pass'] = '' if password == confirm else "Passwords didn't match."
        if ( errs['pass'] or errs['leng'] ):
            return redirect(url_for('auth.reset', ticket=ticket))

        user = User.query.filter_by(email=email).first()
        user.password = hashpw(bytes(password, 'utf-8'), gensalt())
        db.session.commit()

        return redirect(url_for('auth.login'))
