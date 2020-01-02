from flask import render_template, redirect, url_for, request
from LoginSystem.models import User
from LoginSystem import app, db

@app.route('/')
def home ():
    return redirect(
        url_for('auth.login')
    )
