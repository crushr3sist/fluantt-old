from .__init__ import db

from flask_login import UserMixin

class Users(UserMixin,db.Model):
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
    get_id = id

    def __init__(self,email,username,password,name,nickname): 
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.nickname = nickname
    def __repr__(self):
        return f'''
        User(email = {self.email}, username = {self.username}, password = {self.password}, name = {self.name}, nickname = {self.nickname})>
        '''

class BarkMain(db.Model):
    __tablename__ = 'BarkMain'
    Barkid = db.Column(db.Integer(), primary_key=True)
    barkbody = db.Column(db.String(), nullable=False)
    UsersName = db.Column(db.String(), db.ForeignKey('Users.username'), nullable=False,)

    def __init__(self, Barkid, barkbody, UsersName) -> None:
        self.barkid = Barkid
        self.barkbody = barkbody
        self.UsersName = UsersName

