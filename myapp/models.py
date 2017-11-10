from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from myapp import db
from flask_login import UserMixin
from myapp import login_manager
from werkzeug.security import generate_password_hash,check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1
class User(db.Model,UserMixin):
  __tablename__= 'users'
  id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  uid = db.Column(db.String(16),unique = True)
  username = db.Column(db.String(10),unique = True)
  password_hash = db.Column(db.String(128),unique = True)
  email = db.Column(db.String(64),unique = True)
  role = db.Column(db.SmallInteger,default = ROLE_USER)
  pic = db.Column(db.String(24))
  active = db.Column(db.Boolean,default = False)

  def is_authenticate(self):
    return True

  def is_active(self):
    return True

  def is_anonymouse(self):
    return False

  def get_id(self):
    return self.id
  
  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')

  @password.setter
  def password(self,password):
    self.password_hash = generate_password_hash(password) 

  def verify_password(self,password):
    return check_password_hash(self.password_hash,password)

  def generate_confirmation_token(self,expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'],expiration)
    return s.dumps({'active': self.id})

  def confirm(self,token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except:
      return False
    if data.get('active') != self.id:
      return False
    self.active = True
    db.session.add(self)
    db.session.commit()
    return True
    

@login_manager.user_loader
def load_user(id):
  return User.query.get(id)