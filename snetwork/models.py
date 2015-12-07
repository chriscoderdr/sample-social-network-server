"""Declares all the database models"""
from snetwork.core import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Defines the user database model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
