# -*-  coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app, g, request, make_response, flash
from .. import db
from ..models import WebUser, Role
from ..email import send_email
from . import main
from .forms import NameForm
from datetime import datetime
from flask_login import login_required, current_user
from ..decorators import admin_required
from .forms import EditProfileForm, EditProfileAdminForm

#注册的蓝本名main
@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = WebUser.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = WebUser(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #         if current_app.config['FLASKY_ADMIN']:
    #             send_email(current_app.config['FLASKY_ADMIN'], 'New User',
    #                        'mail/new_user', user=user)
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     return redirect(url_for('.index'))

    a = request
    b = current_app
    c = g
    d = session
    ua = request.headers.get('User-Agent')
    response = make_response('<h1>nihaoa</h1>')
    response.set_cookie('answer', '42')

    print(a)
    print(b)
    print(c)
    print(d)
    print(ua)
    return render_template('index.html', name=session.get('name'),
                           current_time=datetime.utcnow(),
                           known=session.get('known', False))


@main.route('/user/<username>')
def user(username):
    #无用户返回404
    user = WebUser.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)



@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = WebUser.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('资料已更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
