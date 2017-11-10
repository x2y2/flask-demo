#-*- coding=utf-8 -*-
#coding=utf8
from flask import render_template,flash,redirect,url_for
from flask_login import login_user,logout_user,current_user,login_required
from ..models import User
from ..forms import LoginForm,AdduserForm
from . import auth
from .. import db
from ..email import send_email
import datetime
import hashlib


@auth.route('/login',methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.verify_password(form.password.data):
      login_user(user,form.remember_me.data)
      cur_user = None
      if current_user.active:
        cur_user = current_user.username
      return render_template('index.html',cur_user=cur_user)
  return render_template('auth/login.html',form=form)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index.index'))

@auth.route('/add_user',methods=['GET','POST'])
def add_user():
  ROLE_ADMIN = '1'
  form = AdduserForm()
  user = User.query.filter_by(username=current_user.username).first()
  if user.role == ROLE_ADMIN:
    if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      email = form.email.data
      role = form.role.data
      register_time = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
      s = ''.join([register_time,username])
      s_md5 = hashlib.md5(s).hexdigest()
      uid = s_md5[0:16]
      #if form.validate_email(email):
      #  flash(u'邮箱已存在')
      #if form.validate_username(username):
      #  flash(u'用户已存在')
      user = User(uid=uid,username=username,password=password,email=email,role=role)
      db.session.add(user)
      db.session.commit()
      token = user.generate_confirmation_token()
      send_email(user.email,'Confirm Your Account','auth/email/confirm',user=user,token=token)
      return 'success'
  else:
    flash('请以管理员身份登录')  
  return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
  cur_user = current_user.username
  if current_user.active:
    return render_template('index.html',cur_user=cur_user)
  if current_user.confirm(token):
    return 'ok'
  else:
    return 'no'
  return render_template('index.html')




