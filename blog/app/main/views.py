from flask import Flask, render_template, session, redirect, url_for, request, flash, abort, current_app, make_response
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Students, User


@main.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(
                    request.form['name'],
                    request.form['city'],
                    request.form['addr'])

            db.session.add(student)
            db.session.commit()

            flash('Record was succesfully added')
            return redirect(url_for('main.index'))
    return render_template('show_all.html', title='Home', students=Students.query.all())



@main.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            flash('This email now register!')
            return redirect(url_for('main.register'))
        else:
            user = User(email= request.form['email'], username = request.form['username'], password = request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Registration.')
            return redirect(url_for('main.index'))
    return render_template('register.html', title = 'Registration')