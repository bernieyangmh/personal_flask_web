# -*-  coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app, g, request, make_response
from .. import db
from ..models import WebUser
from ..email import send_email
from . import main
from .forms import NameForm
from datetime import datetime

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
