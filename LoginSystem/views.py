from flask import render_template, redirect, url_for, request
from LoginSystem import app, db
from LoginSystem.models import User

@app.route('/')
def home ():
    return redirect(
        url_for('login')
    )

@app.route('/login', methods=['POST', 'GET'])
def login ():
    if ( request.method == 'POST' ):
        username = request.form['user']
        password = request.form['pass']

        print(f'Username: {username}')
        print(f'Password: {password}')

    return render_template(
        'login.html',
        title='Login',
        script='/static/js/index.js'
    )
