from flask import Blueprint, render_template, redirect, request
from LoginSystem.models import User, add_admin

auth = Blueprint('auth', __name__)

@auth.route('/login')
def render_login ():
    return render_template(
        'login.html',
        title='Sign in',
        script='/static/js/index.js'
    )


@auth.route('/login', methods=['POST', 'GET'])
def login ():
    if ( request.method == 'POST' ):
        _user = request.form['user']
        _pass = request.form['pass']
        # _keep = request.form['keep']

        user = User.query.filter_by(username=_user).first()
        print(user.id)
        print(user.username)
        print(user.email)
        print(user.password)

    return render_template(
        'login.html',
        title='Sign in',
        script='/static/js/index.js'
    )
