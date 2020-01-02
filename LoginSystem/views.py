from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from LoginSystem.models import User
from LoginSystem import app, db

@app.route('/')
@login_required
def home ():
    return current_user.username

