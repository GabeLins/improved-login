# Flask Rendering Modules
from flask import Blueprint, render_template, redirect, abort
from flask import request, flash, url_for

# Flask Login Modules
from flask_login import login_user, login_required
from flask_login import logout_user, current_user

# Cryptography and tokens
from itsdangerous import URLSafeTimedSerializer
from bcrypt import hashpw, checkpw, gensalt

# Application Modules
from LoginSystem import db, settings
from LoginSystem.models import User
from LoginSystem.email import send_mail


serializer = URLSafeTimedSerializer(settings['secret_key'])
auth = Blueprint('auth', __name__)
errs = {}

# Render functions
# Login Page
@auth.route('/login')
def render_login ():
    errors = dict(errs)
    errs.clear()

    # Check if user is authenticated
    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'login.html',
        title='Sign in',
        errors=errors
    )


# Sign Up Page
@auth.route('/register')
def render_register ():
    errors = dict(errs)
    errs.clear()

    # Check if user is authenticated
    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'register.html',
        title='Sign up',
        errors=errors
    )


# Password Recovery Page
@auth.route('/recover')
def render_recover ():
    errors = dict(errs)
    errs.clear()

    # Check if user is authenticated
    if ( current_user.is_authenticated ):
        return redirect(url_for('home'))

    return render_template(
        'recover.html',
        title='Recover Account',
        errors=errors
    )



# Processing functions
# Login authentication
@auth.route('/login', methods=['POST'])
def login ():
    if ( request.method == 'POST' ):
        # Get login form data
        _mail = request.form['contact'] # TODO: Add phone number support
        _pass = request.form['password']
        _keep = 'remember' in request.form

        # Get user from database
        user = User.query.filter_by(email=_mail).first()
        
        # Check if the user and password combination match
        if ( user and checkpw(bytes(_pass, 'utf-8'), user.password) ):
            # Check if user isn't verified
            if ( not user.verified ):
                errs['vrfy'] = 'Please, verify your email.'
                return redirect(url_for('auth.login'))

            # Return a successful login
            login_user(user, remember=_keep)
            return redirect(url_for('home'))
        
        # Return an error if password and user combination doesn't match
        else:
            errs['logn'] = 'Invalid email or password.'
            return redirect(url_for('auth.login'))


# Sign up authentication
@auth.route('/register', methods=['POST', 'GET'])
def register ():
    if ( request.method == 'POST' ):
        # Get sign up form data
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        email = request.form['contact'] # TODO: Add phone number support
        agree = 'agree' in request.form

        # Return an error if the user didn't agree with the terms of service.
        if ( not agree ):
            errs['term'] = 'Please, check the agreement box.'
            return redirect(url_for('auth.register'))

        # Check if username is valid
        errs['user'] = (
            ''
            if not User.query.filter_by(username=username).first()
            else 'Username already in use.'
        )

        # Check if email address is valid
        errs['mail'] = (
            ''
            if not User.query.filter_by(email=email).first()
            else 'Email already in use.'
        )

        # Check if password is at least 8 characters long
        errs['leng'] = (
            ''
            if len(password) >= 8
            else 'Password must be at least 8 characters long.'
        )

        # Check if password and confirmation match
        errs['pass'] = '' if password == confirm else "Passwords didn't match."

        # Check if first name or last name are filled
        errs['last'] = '' if last_name else 'Empty field.'
        errs['name'] = '' if first_name else 'Empty field.'

        # Check if any error has occured
        if ( not any(errs.values()) ):
            # Create a new User encrypting its password with the bcrypt module
            user = User(
                username=username,
                password=hashpw(bytes(password, 'utf-8'), gensalt()),
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            # Add the user to the database and commit changes
            db.session.add(user)
            db.session.commit()

            # Generate an email verification token 
            ticket = serializer.dumps(email, salt='verify-account')

            # Send the verification token to the user email
            send_mail(
                (request.url_root, request.headers['Host']), 
                ticket, email, 'verify'
            )

            # TODO: Create an endpoint where the user can use a 6 digit 
            # verification PIN
            return redirect(url_for('auth.login'))

        return redirect(url_for('auth.register'))


# Email Verification
@auth.route('/verify/<ticket>', methods=['POST', 'GET'])
def verify ( ticket: str ):
    try:
        # Check if the specified token is valid and hasn't expired
        email = serializer.loads(ticket, salt='verify-account', max_age=86400)
    except:
        # Return an error if the token is invalid or has expired
        return abort(401)

    if ( request.method == 'GET' ):
        # Verify the user on the database
        user = User.query.filter_by(email=email).first()
        user.verified = True
        db.session.commit()

        return redirect(url_for('auth.login'))


# Logout
@auth.route('/logout')
@login_required
def logout ():
    logout_user()
    return redirect(url_for('auth.login'))


# Password Recovery
@auth.route('/recover', methods=['POST', 'GET'])
def recover ():
    if ( request.method == 'POST' ):
        # Get user account email
        email = request.form['contact']

        # Check if email is valid
        errs['recv'] = (
            ''
            if User.query.filter_by(email=email).first()
            else 'Invalid email address.'
        )

        # Return an error if the email is invalid
        if ( errs['recv'] ):
            return redirect(url_for('auth.recover'))
        
        # Generate a password reset token
        ticket = serializer.dumps(email, salt='reset-password')

        # Send the password reset token to the user email address
        send_mail(
            (request.url_root, request.headers['Host']), 
            ticket, email, 'reset'
        )

    return redirect(url_for('auth.login'))


# Password Reset
@auth.route('/recover/token/<ticket>', methods=['POST', 'GET'])
def reset ( ticket: str ):
    errors = dict(errs)
    errs.clear()

    try:
        # Check if the specified reset token is valid and hasn't expired
        email = serializer.loads(ticket, salt='reset-password', max_age=300)
    except:
        # Return an error if the token is invalid or has expired
        return abort(401)

    # Render the new password form
    if ( request.method == 'GET' ):
        return render_template(
            'reset.html',
            title=email,
            errors=errors
        )

    # Get user data
    if ( request.method == 'POST' ):
        # Get new password
        password = request.form['password']
        confirm = request.form['confirm']

        # Check if password length is valid
        errs['leng'] = (
            ''
            if len(password) >= 8
            else 'Password must be at least 8 characters long.'
        )

        # Check if password and confirmation match
        errs['pass'] = '' if password == confirm else "Passwords didn't match."
        if ( errs['pass'] or errs['leng'] ):
            # Reload page if any error occurs
            return redirect(url_for('auth.reset', ticket=ticket))

        # Update user information on the database
        user = User.query.filter_by(email=email).first()
        user.password = hashpw(bytes(password, 'utf-8'), gensalt())
        db.session.commit()

        return redirect(url_for('auth.login'))
