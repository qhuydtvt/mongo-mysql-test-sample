import pymysql

class MySQLHelper:
  def __init__(self, conn):
    self.conn = conn
  
  def find_one(self, sql_command):
    with self.conn.cursor() as cursor:
      # Read a single record
      cursor.execute(sql_command)
      result = cursor.fetchone()
      return result
  
  def find_all(self, sql_command):
    with self.conn.cursor() as cursor:
      # Read a single record
      cursor.execute(sql_command)
      result = cursor.fetchall()
      return result 