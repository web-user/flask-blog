from flask import Flask, render_template, session, redirect, url_for, request, flash, abort, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import admin
from .. import db
from ..models import User, Post
from ..form import PostForm
from functools import wraps
from flask import g, request, redirect, url_for

@admin.route('/admin', methods = ['GET', 'POST'])
@login_required
def admin():
    form = PostForm()
    error = None
    if request.method == 'POST' and form.validate():
        print(form.body.data)
        print('MMM----------NNNN')
        post = Post(body=form.body.data, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
        flash('Invalid username or password.')
    return render_template('admin.html', title='Admin', form=form)


