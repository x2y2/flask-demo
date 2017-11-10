from flask import render_template,flash,request
from flask_login import current_user
from . import index

@index.route('/',methods=['GET','POST'])
@index.route('/index',methods=['GET','POST'])
def index():
  rv = request.data
  return rv
  #cur_user = current_user.username
  #return render_template('index.html')

