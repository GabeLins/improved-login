from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from LoginSystem.models import User
from LoginSystem import app, db

@app.route('/')
@login_required
def home ():
    return render_template(
        'index.html',
        title='Index - {}'.format(current_user.username),
        user=current_user
    )


@app.errorhandler(401)
@app.errorhandler(404)
def page_not_found ( error ):
    return render_template(
        'error.html',
        title=error,
        code=error.code
    )
