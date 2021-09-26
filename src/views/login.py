from src.models import Users
from src import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))