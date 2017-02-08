# -*-  coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, WebUser

class NameForm(FlaskForm):
    name = StringField(u'你叫什么名字?', validators=[DataRequired()])
    submit = SubmitField(u'提交')



class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField(u'邮箱地址', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField(u'是否认证')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        #从role表中取出所有角色当作SelectField的选择项
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                WebUser.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                WebUser.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已使用')

class PostForm(FlaskForm):
    title = StringField(u'标题', validators=[Length(0, 64)])
    body = TextAreaField(u"内容", validators=[DataRequired()])
    submit = SubmitField(u'提交')