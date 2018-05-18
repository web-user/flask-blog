import os
from datetime import datetime
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin, LoginManager
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager, Shell
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import Column, Integer, String

from app import create_app
from flask import current_app, request, url_for
from sqlalchemy import Column, Integer, String


login_manager = LoginManager()

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.getenv('FLASK_CONFIG'))

manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'blog_db'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=False)
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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')