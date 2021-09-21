from flask_login.utils import login_user, logout_user
from src.forms import LoginForm, Register
from flask import Blueprint, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect
auth = Blueprint('authentication', __name__)
from src.models import *

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        request.form.get('email')
        userReg = Users(
            request.form['email'],
            request.form['username'],
            request.form['password'], 
            request.form['name'], 
            request.form['nickname'])
        db.session.add(userReg)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', form=Register())

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'Post':
        form = LoginForm()
        if form.validate_on_submit():
            login_user(Users)
            return redirect(f'/{Users.username}/home')
    return render_template('login.html', form=LoginForm())


@auth.route('/logout', methods=['POST','GET'])
@login_required
def logout():
    if Users.is_authenticated:
        logout_user(Users)
        return redirect('/login')
    return render_template('login.html')


@auth.route('/<user>/home')
@login_required
def userHome(user):
    return user
