# Flask Rendering Modules
from flask import render_template, redirect, url_for, request

# Flask Login Modules
from flask_login import login_required, current_user

# Application Modules
from LoginSystem.models import User
from LoginSystem import app, db


# Home page route
# TODO: Set this do /profile, and create an open home page
@app.route('/')
@login_required
def home ():
    return render_template(
        'index.html',
        title='Index - {}'.format(current_user.username),
        user=current_user
    )


# Error handlers
@app.errorhandler(401)
@app.errorhandler(404)
def page_not_found ( error ):
    return render_template(
        'error.html',
        title=error,
        code=error.code
    )
