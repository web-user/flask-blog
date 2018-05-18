from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from sqlalchemy import Column, Integer, String


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    email = db.Column(String(120), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    title= db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % self.title