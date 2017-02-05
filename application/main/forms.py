# -*-  coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField(u'你叫什么名字?', validators=[DataRequired()])
    submit = SubmitField(u'提交')
