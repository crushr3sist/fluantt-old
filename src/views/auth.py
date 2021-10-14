import json, os, requests
from flask.helpers import url_for
from werkzeug.security import check_password_hash
from src.forms import LoginForm, Register
from flask import Blueprint, render_template, request, session
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import redirect
from authlib.integrations.requests_client import OAuth2Session

GOOGLE_CLIENT_ID = "1051638467361-9u2jc677sacg293dg1hso07bnkt0eagt.apps.googleusercontent.com"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_CLIENT_SECRET = "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"
auth = Blueprint('authentication', __name__)

from src.__init__ import oauth
from src.__init__ import db 

from src.models import _googleAuthUser, _localuser

google = oauth.register(
    name='google',
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    prompt='consent'

)
client = OAuth2Session(GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,)



@auth.route("/")
def index():
    return render_template('index.html')

@auth.route('/register', methods=['POST','GET'])
def IntRegister():
    if request.method == 'POST':
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

@auth.route('/authorize')
def authorize():
    google = oauth.create_client('google') 
    token = google.authorize_access_token() 
    session['token'] = token
    session['google'] = google
    resp = google.get('userinfo')  
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session.perminant = True
    if user:
        exists = _googleAuthUser.query.filter_by(email = user.email).first()
        userObj = _googleAuthUser(uid = user.sub , name = user.name, email = user.email, profile_pic = user.picture)
        if not exists:
            db.session.add(userObj)
            db.session.commit()
            newUserObj = _googleAuthUser.query.filter_by(email = user.email).first()
            newUserObj.is_active = True
            login_user(newUserObj)
            return redirect('/user/google')
        else:
            exists.is_active = True
            login_user(exists)
            return redirect('/user/google')
    else:
        return redirect('/googlelogin')    
        
@auth.route('/googlelogin')
def gglRedirect():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authentication.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            CurrentUser = _localuser.query.filter_by(username=form.username.data).first()
            print(CurrentUser)
            if CurrentUser and CurrentUser.verify_password(form.password.data):  
                CurrentUser.is_active = True
                login_user(CurrentUser)
                print(login_user(CurrentUser))
                return redirect(f'/user/local')
            else:
                return f'{CurrentUser.verify_password(form.password.data)}'
    else:
        return render_template('auth/login.html', form=LoginForm())

@auth.route('/user/local')
def userLocal():
    k = [current_user.email,current_user.username,current_user.password,current_user.name,current_user.nickname]
    return render_template('personal/profilePage.html', objec = k)

@auth.route('/user/google')
def userGoogle():
    k = [current_user.uid,current_user.name,current_user.email,current_user.profile_pic]
    return render_template('personal/profilePage.html', objec = k)

@auth.route('/session')
def route():
    return session

@auth.route('/googlelogout')
def googlelogout():
    for key in list(session.keys()):
        session.pop(key)
    currentToken = session['token'] 
    currentClient = session['google']
    token_endpoint = 'https://127.0.0.1:8080/authorize'
    
    currentClient.revoke_token(token_endpoint, token=currentToken)
    currentClient.introspect_token(token_endpoint, token=currentToken)

    return redirect('/session')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/googlelogout')

'''
      
   



k = [current_user.id,current_user.email,current_user.username,current_user.password,current_user.name,current_user.nickname]
'''