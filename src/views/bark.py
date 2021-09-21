from flask import Blueprint, render_template
from flask_login import login_required

bark = Blueprint('main', __name__)

@bark.route('/')
def index():
    return render_template('index.html')

@bark.route('/register')
def register():
    return render_template('register.html')

@bark.route('/login')
def login():
    return render_template('login.html')


        