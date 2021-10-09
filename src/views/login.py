from src.models import Users
from src import *
import os, json, sys


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authentication.login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))