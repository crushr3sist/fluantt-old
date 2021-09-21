from flask_wtf import FlaskForm
from wtforms import *

class Register(FlaskForm):
    email    = StringField('email')
    username = StringField('username')
    password = StringField('password')
    name     = StringField('name')
    nickname = StringField('nickname')
    registerSub = SubmitField('registerSub')

class LoginForm(FlaskForm):
    
    username = StringField('username')
    password = StringField('password')
    registerSub = SubmitField('registerSub')