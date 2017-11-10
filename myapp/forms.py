#-*- coding=utf-8 -*-
#coding=utf-8

from wtforms import BooleanField,TextField,PasswordField,SubmitField,StringField,ValidationError,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf import FlaskForm
from myapp.models import User


class LoginForm(FlaskForm):
  username = TextField(u'姓名',validators=[DataRequired(message=u'用户名不能为空'),Length(4,10)])
  password = PasswordField(u'密码',validators=[DataRequired(message=u'密码不能为空')])
  remember_me = BooleanField(u'记住我',default='checked')
  submit = SubmitField(u'登录')

class AdduserForm(FlaskForm):
  username = TextField(u'用户昵称',validators=[DataRequired(message=u'用户名不能为空'),Length(4,10)])
  password = PasswordField(u'用户密码',validators=[DataRequired(message=u'密码不能为空'),
                                              EqualTo('confirm',message=u'密码不一致')])
  confirm = PasswordField(u'确认密码',validators=[DataRequired(message=u'密码不能为空')])
  email = StringField(u'用户邮箱',validators=[DataRequired(),Length(6,64),Email()])
  role = SelectField(u'用户角色',choices = [('0','guest'),('1','admin')])
  submit = SubmitField(u'注册')

  def validate_email(self,field):
    if User.query.filter_by(email = field).first():
      raise ValidationError(u'邮箱已注册')

  def validate_username(self,field):
    if User.query.filter_by(username = field).first():
      raise ValidationError(u'用户已存在')