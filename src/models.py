from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from .__init__ import db

from flask_login import UserMixin


class _localuser(UserMixin,db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    nickname = db.Column(db.String(), nullable=False)

    is_authenticated = False
    is_active = False
    is_anonymous = False

    def get_id(self):
        return self.id
    def is_authenticated(self):
        return self.authenticated

    def __init__(self,email,username,password,name,nickname): 
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.nickname = nickname
        
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class _googleAuthUser(UserMixin, db.Model):

    id_ = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    profile_pic = db.Column(db.String(), nullable=False)

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = generate_password_hash(email)
        self.profile_pic = profile_pic

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated
    
    def verify_user(self, email):
        return check_password_hash(self.email, email)

class BarkMain(db.Model):
    __tablename__ = 'BarkMain'
    Barkid = db.Column(db.Integer(), primary_key=True)
    barkbody = db.Column(db.String(), nullable=False)
    UsersName = db.Column(db.String(), db.ForeignKey('Users.username'), nullable=False,)

    def __init__(self, Barkid, barkbody, UsersName) -> None:
        self.barkid = Barkid
        self.barkbody = barkbody
        self.UsersName = UsersName
