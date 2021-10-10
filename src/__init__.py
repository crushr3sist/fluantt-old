
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login.login_manager import LoginManager
from src.views.auth import auth
from src.views.bark import bark
from authlib.integrations.flask_client import OAuth



def create_app():
    appVar = Flask(__name__)
    appVar.secret_key = '>%P5z#vcQ7' 
    appVar.register_blueprint(auth)
    appVar.register_blueprint(bark)
    
    appVar.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/fluantt.sqlite3'
    appVar.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return appVar

app = create_app()
oauth = OAuth(app)
db = SQLAlchemy(app)




