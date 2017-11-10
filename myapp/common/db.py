from myapp import mysql

class db:
  @staticmethod
  def query(sql):
    cur = mysql.connection.cursor()
    cur.execute(sql)
    rv = cur.fetchall()
    cur.close()
    return rv
  
  @staticmethod
  def execute(sql):
    cur = mysql.connection.cursor()
    cur.execute(sql)
    cur.commit()
    cur.close()
  

