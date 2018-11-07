
from eQSolve import db
from sqlalchemy.schema import PrimaryKeyConstraint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from datetime import datetime
from eQSolve.Config import Config
from eQSolve import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(64), index=True, unique=True)
    rank = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None


class Equation(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    eq1 = db.Column(db.String(32))
    eq2 = db.Column(db.String(32))
    sol = db.Column(db.String(128))

class UserToEq(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    eqId = db.Column(db.Integer, db.ForeignKey("equation.id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (PrimaryKeyConstraint(userId, eqId),)




