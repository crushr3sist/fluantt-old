from flask_login.utils import login_user, logout_user
from werkzeug.security import check_password_hash
from src.forms import LoginForm, Register
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect
# from werkzeug import check_password_hash


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
    return render_template('auth/register.html', form=Register())

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if not user:
                return redirect('/login')
            else:
                user.is_active = True
                login_user(user)
                return redirect(f'/{user.username}/home')
    else:
        return render_template('auth/login.html', form=LoginForm())

@auth.route('/user')
@login_required
def userQuery():
    k = [
        current_user.email,
    current_user.username,
    current_user.password,
    current_user.name,
    current_user.nickname
    ] 

    return render_template('personal/profilePage.html', objec = k)

@auth.route('/logout', methods=['POST','GET'])
@login_required
def logout():
    if Users.is_authenticated:
        logout_user()
        return redirect('/login')
    return render_template('login.html')


@auth.route('/<user>/home')
@login_required
def userHome(user):
    return user
