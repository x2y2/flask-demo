from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config

db =  SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
mail = Mail()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)


  from admin import admin
  app.register_blueprint(admin)
  
  from index import index
  app.register_blueprint(index) 

  from auth import auth
  app.register_blueprint(auth)

  return app
