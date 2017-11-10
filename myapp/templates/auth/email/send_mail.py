from threading import Thread 
from flask import current_app
from flask_mail import Mail,Message

g_mail = None
def send_async_email(app,msg):
  global g_mail
  with app.app_context():
    g_mail.send(msg)

def send_mail(to,subject,html):
  app = current_app._get_current_object()
  g_mail = Mail(app)
  msg = Message(subject=subject,recipients=to,html=html)
  t = Thread(target=send_async_email,args=[app,msg])
  t.start()
  return t