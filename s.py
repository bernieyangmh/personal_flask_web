# -*-  coding:utf-8 -*-
from threading import Thread
from flask import Flask, render_template
from flask import request
from flask import current_app
from flask import g
from flask import session, make_response, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import FlaskForm
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Mail, Message

import os

basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://work:123@localhost/flask_dev'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'nichai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flaskyang]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <{}>'.format(app.config['MAIL_USERNAME'])
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        print'finished'

# Todo celery
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = WebUser.query.filter_by(username=form.name.data).first()
        if user is None:
            user = WebUser(username=form.name.data)
            db.session.add(user)
            session['know'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        old_name = session.get('name')
        return redirect(url_for('index'))
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
    print(basedir)
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), know=session.get('know', False))

@app.route('/<user>/<name>')
def user(name, user):
    print name
    print user
    forloop = [1,2,3,4,5,6]
    return render_template('user.html', name=name, user=user, forloop=forloop)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

def make_shell_context():
    return dict(app=app, db=db, User=WebUser, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)



class NameForm(FlaskForm):
    name = StringField(u'你叫什么名字?', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class WebUser(db.Model):
    __table__name = 'webusers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('WebUser', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)




if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
    db.create_all()