class Config:
  SECRET_KEY = 'ssdfdfdffd'
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  
  @staticmethod
  def init_app(app):
    pass

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI =  'mysql://wangpei:123456@127.0.0.1/test?charset=utf8mb4'
  FLASKY_MAIL_SENDER = 'p.wang@avid.ly'
  MAIL_SERVER = 'smtp.avid.ly'
  MAIL_PORT = 25
  MAIL_USERNAME = 'p.wang@avid.ly'
  MAIL_PASSWORD = 'Avidly0327'

config = {'Production': ProductionConfig}
