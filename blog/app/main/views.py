from flask import Flask, render_template, session, redirect, url_for, request, flash, abort, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import main
from .. import db
from ..models import User, Post
from ..form import UserLoginForm, PostForm


@main.route('/', methods = ['GET', 'POST'])
def home():
    posts = Post.query.all()
    return render_template('show_all.html', title='Home', posts=posts)


@main.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            flash('This email now register!')
            return redirect(url_for('main.register'))
        else:
            user = User(email= request.form['email'], name = request.form['username'], password = request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Registration.')
            return redirect(url_for('main.home'))
    return render_template('register.html', title = 'Registration')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(name=form.user.name).first()
        if user:
            if login_user(user):
                return redirect(url_for('main.home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':

        post.body = request.form['body']
        post.title = request.form['title']

        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('main.home'))
    return render_template('edit_post.html', post = post )


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))