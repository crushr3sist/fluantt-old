import json
import os
from flask_login.utils import login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
from werkzeug.security import check_password_hash
from src.forms import LoginForm, Register
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

import requests
# from werkzeug import check_password_hash

GOOGLE_CLIENT_ID = "1051638467361-9u2jc677sacg293dg1hso07bnkt0eagt.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

oAuthClient = WebApplicationClient(GOOGLE_CLIENT_ID)

auth = Blueprint('authentication', __name__)
from src.models import *

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@auth.route("/")
def index():

    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.email, current_user.username, current_user.password, current_user.name,current_user.nickname
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@auth.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        request.form.get('email')
        userReg = _localuser(
            request.form['email'],
            request.form['username'],
            request.form['password'], 
            request.form['name'], 
            request.form['nickname'])
        db.session.add(userReg)
        db.session.commit()
        return redirect('/login')
    return render_template('auth/register.html', form=Register())

@auth.route('/login/callback')
def callback():
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    token_url, headers, body = oAuthClient.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        code = code
    )
    token_response = requests.post(
        token_url,
        headers = headers,
        data = body, 
        auth = (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    oAuthClient.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = oAuthClient.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    return userinfo_response
    # if userinfo_response.json().get("email_verified"):
    #     unique_id = userinfo_response.json()["sub"]
    #     users_email = userinfo_response.json()["email"]
    #     picture = userinfo_response.json()["picture"]
    #     users_name = userinfo_response.json()["given_name"]

    #     return [unique_id, users_email, picture, users_name]

    # else:
    #     return "User email was not available or not verified by Google.", 400
    


@auth.route('/login', methods=['POST','GET'])
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = oAuthClient.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)
    # if request.method == 'POST':
    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         user = _localuser.query.filter_by(username=form.username.data).first()
    #         if user and user.verify_password(form.password.data):  
    #             user.is_active = True
    #             login_user(user)
    #             return redirect(f'/{user.username}/home')
    #         else:
    #             return f'{user.verify_password(form.password.data)}'
    # else:
    #     return redirect('/login')

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
    if _localuser.is_authenticated:
        logout_user()
        return redirect('/login')
    return render_template('login.html')


@auth.route('/<user>/home')
@login_required
def userHome(user):
    return user

'''
'''