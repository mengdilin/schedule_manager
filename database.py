import mysql.connector
from mysql.connector import errorcode


cnx = mysql.connector.connect(user='ml3567'
  , password='database'
  ,host='cs4111.cr3ixrw5cu0f.us-west-2.rds.amazonaws.com'
  ,database='cs4111')
cursor = cnx.cursor()

def execute_query(query):
  cursor.execute(query)
  return cursor.fetchall()

if __name__ == '__main__':
  data = execute_query(("SELECT * FROM Users"))
  print data
