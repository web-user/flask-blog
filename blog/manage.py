import time
import os
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import UserMixin, AnonymousUserMixin, LoginManager
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager, Shell
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from sqlalchemy import Column, Integer, String



login_manager = LoginManager()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager.init_app(app)

DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'


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




def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


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


def database_initialization_sequence():
    db.create_all()
    db.session.rollback()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('show_all.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            flash('This email now register!')
            return redirect(url_for('register'))
        else:
            user = User(email= request.form['email'], name = request.form['username'], password = request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Registration.')
            return redirect(url_for('home'))
    return render_template('register.html', title = 'Registration')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email = request.form['email']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user, request.form['remember_me'])

            current_user.name = request.form['name']
            current_user.location = request.form['email']
            db.session.add(current_user)

            return redirect(url_for('login'))
        flash('Invalid username or password.')

    return render_template('login.html', title = 'Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
