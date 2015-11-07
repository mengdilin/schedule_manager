import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


cnx = mysql.connector.connect(user='ml3567'
  , password='database'
  ,host='cs4111.cr3ixrw5cu0f.us-west-2.rds.amazonaws.com'
  ,database='cs4111_new')

def execute_query(query):
  cursor.execute(query)
  return cursor.fetchall()

def create_user(first_name, last_name, user_username, password):
  cursor = cnx.cursor()
  cursor.execute("SELECT username FROM Users WHERE username=%s", (user_username,))
  if len(cursor.fetchall()) == 0:
    cursor.execute("INSERT INTO Users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, user_username, password))
    cnx.commit()
    cursor.close()
    return True
  cursor.close()
  return False

def create_organization(name, org_username, password):
  cursor = cnx.cursor()
  cursor.execute("SELECT username FROM Organizations WHERE username=%s", (org_username,))
  if len(cursor.fetchall()) == 0:
    cursor.execute("INSERT INTO Organizations (name, org_username, password) VALUES (%s, %s, %s)", (name, org_username, password))
    cnx.commit()
    cursor.close()
    return True
  cursor.close()
  return False

def create_event(name, date, start_time, end_time, description, image, org_name, building, room):
  return True

def create_invitation():
  return True

def create_decision():
  return True

def create_location():
  return True

def create_category(name):
  return True

def user_login(user_username, password):
  cursor.execute("SELECT password FROM Users WHERE username=%s AND password=%s", (user_username, password))
  if len(cursor.fetchall()) !=0:
    return True
  return False

def organization_login(org_username, password):
  cursor.execute("SELECT password FROM Organizations WHERE username=%s AND password=%s", (org_username, password))
  if len(cursor.fetchall()) !=0:
    return True
  return False

def participates_in_org(user_username, org_username):
  cursor.execute("""INSERT INTO Users_Organizations (user_username, org_username)
                    VALUES (%s, %s)""", (user_username, org_username))

def users_in_organization(org_username):
  cursor.execute("""SELECT first_name, last_name
                    FROM Users, Users_Organizations
                    WHERE Users_Organizations.org_username=%s AND Users.username = Users_Organizarions.user_username""", (user_username))
  return cursor.fetchall()

def organizations_user_is_in(user_username):
  cursor.execute("""SELECT Organizations.name
                    FROM Organizations, Users_Organizations
                    WHERE Users_Organizations.user_username=%s AND Organizations.username = Users_Organizations.org_username""", (user_username))
  return cursor.fetchall()

def events_created_by_org(org_username):
  cursor.execute("SELECT name FROM Creates_Events WHERE org_username=%s", (org_username))
  return cursor.fetcall()

def get_users_invites(user_username):
  cursor.execute("""SELECT Creates_Events.name
                    FROM Creates_Events, Invitations
                    WHERE Invitations.user_username=%s AND Creates_Events.eid = Invitations.eid""", (user_username))
  return cursor.fetchall()

def get_events_in_category(category):
  cursor.execute("""SELECT Creates_Events.name
                    FROM Creates_Events, Events_Categories
                    WHERE Events_Categories.name=%s AND Creates_Events.eid = Events_Categories.eid""", (category))
  return cursor.fetchall()

def user_past_events(user_username):
  present = datetime.now()
  cursor.execute("""SELECT Creates_Events.name
                    FROM Creates_Events, Invitations, Decides_Decisions
                    WHERE Invitations.user_username=%s AND Decides_Decisions.user_username=%s AND Decides_Decisions.status_id=1
                          AND Creates_Events.eid = Invitations.eid AND ((Creates_Events.date < present.date()) OR
                          (Creates_Events.date = present.date() AND Creates_Events.end_time < present.time()))""", (user_username, user_username))
  return cursor.fetchall()

def user_future_events(user_username):
  present = datetime.now()
  cursor.execute("""SELECT Creates_Events.name
                    FROM Creates_Events, Invitations, Decides_Decisions
                    WHERE Invitations.user_username=%s AND Decides_Decisions.username=%s AND Decides_Decisions.status_id=1
                          AND Creates_Events.eid = Invitations.eid AND ((Creates_Events.date > present.date()) OR
                          (Creates_Events.date = present.date() AND Creates_Events.start_time > present.time()))""", (user_username, user_username))
  return cursor.fetchall()

def decide_on_invite(user_username, eid, decision):
  return True

if __name__ == '__main__':
  #query = "SELECT username FROM Users WHERE username=%s"
  #cursor.execute(query, ('mengdilin',))
  #print cursor.fetchall()
  print organization_login("broomclub", "broomslife ")
