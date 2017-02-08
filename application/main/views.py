# -*-  coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app, g, request, make_response, flash
from .. import db
from ..models import WebUser, Role, Post, Permission
from ..email import send_email
from . import main
from .forms import NameForm
from datetime import datetime
from flask_login import login_required, current_user
from ..decorators import admin_required
from .forms import EditProfileForm, EditProfileAdminForm, PostForm

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

    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        #_get_current_object拿到真正的用户对象
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int) #默认值int 1 pagination为一个对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', name=session.get('name'),
                           current_time=datetime.utcnow(),
                           form=form, posts=posts,
                           )


@main.route('/user/<username>')
def user(username):
    #无用户返回404
    @main.route('/user/<username>')
    def user(username):
        user = WebUser.query.filter_by(username=username).first_or_404()
        posts = user.posts.order_by(Post.timestamp.desc()).all()
        return render_template('user.html', user=user, posts=posts)


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
