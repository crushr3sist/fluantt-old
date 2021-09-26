from flask_login.utils import login_user, logout_user
from werkzeug.security import check_password_hash
from src.forms import LoginForm, Register
from flask import Blueprint, render_template, request
from flask_login import login_required
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
    return render_template('register.html', form=Register())

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        print('got past: form declaration')
        if form.validate_on_submit():
            print('got past: validation_on_submit function')
            user = Users.query.filter_by(username=form.username.data).first()
            print('got past: user variable declaration')
            if not user or not check_password_hash(user.password, form.password.data):
                return redirect('/login')
            login_user(user)
            print('got past: login user function')
            return redirect(f'/{form.username.data}/home')
    else:
        return render_template('login.html', form=LoginForm())

@auth.route('/user')
def userQuery():
    user = Users.query.filter_by(username='admin').first()
    print(user.email)
    return str(user)

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
