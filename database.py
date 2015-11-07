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
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT username FROM Users WHERE username=%s", (user_username,))
    if len(cursor.fetchall()) == 0:
      cursor.execute("INSERT INTO Users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, user_username, password))
      cnx.commit()
      cursor.close()
      return True
    cursor.close()
    return False
  except mysql.connector.Error as err:
    return False

def create_organization(name, org_username, password):
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT username FROM Organizations WHERE username=%s", (org_username,))
    if len(cursor.fetchall()) == 0:
      cursor.execute("INSERT INTO Organizations (name, username, password) VALUES (%s, %s, %s)", (name, org_username, password))
      cnx.commit()
      cursor.close()
      return True
    cursor.close()
    return False
  except mysql.connector.Error as err:
    return False

def create_event(name, date, start_time, end_time, description, image, org_name, building, room):
  try:
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO Creates_Events (name, date, start_time, end_time, description, image, org_username, building, room) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, date, start_time, end_time, description, image, org_name, building, room))
    cnx.commit()
    cursor.lastrowid;
    cursor.close()
  except mysql.connector.Error as err:
    return False
  return True

def create_invitation(user_username, org_username, eid):
  try:
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO Invitations (user_username, org_username, eid) VALUES (%s, %s, %s)", (user_username, org_username, eid))
    cnx.commit()
    cursor.close()
    return True
  except mysql.connector.Error as err:
    return False

def create_location(building, room):
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT building, room FROM Locations WHERE building=%s AND room=%s", (building, room))
    if len(cursor.fetchall()) == 0:
      cursor.execute("INSERT INTO Locations (building, room) VALUES (%s, %s)", (building, room))
      cnx.commit()
      cursor.close()
      return True
    cursor.close()
    return False
  except mysql.connector.Error as err:
    return False

def create_category(name):
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT name FROM Categories WHERE name=%s", (name,))
    if len(cursor.fetchall()) == 0:
      cursor.execute("INSERT INTO Categories (name) VALUES (%s)", (name,))
      cnx.commit()
      cursor.close()
      return True
    cursor.close()
    return False
  except mysql.connector.Error as err:
    return False

def create_event_category(eid, name):
  try:
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO Events_Categories (name, eid) VALUES (%s, %s)", (name, eid))
    cnx.commit()
    cursor.close()
    return True
  except mysql.connector.Error as err:
    return False

def find_eid(name, date, start_time, end_time, org_name, building, room):
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT eid FROM Creates_Events WHERE name=%s AND date=%s AND start_time=%s AND end_time=%s AND org_username=%s AND building=%s AND room=%s",(name, date, start_time, end_time, org_name, building, room))
    return cursor.fetchall()
  except mysql.connector.Error as err:
    return False

def events_at_same_time(name, date, start_time, end_time, org_name, building, room):
  eid = find_eid(name, date, start_time, end_time, org_name, building, room)
  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM Creates_Events WHERE date=%s AND start_time=%s", (date, start_time))
  return cursor.fetchall()

def user_login(user_username, password):
  cursor = cnx.cursor()
  cursor.execute("SELECT password FROM Users WHERE username=%s AND password=%s", (user_username, password))
  if len(cursor.fetchall()) !=0:
    return True
  return False

def organization_login(org_username, password):
  cursor = cnx.cursor()
  cursor.execute("SELECT password FROM Organizations WHERE username=%s AND password=%s", (org_username, password))
  if len(cursor.fetchall()) !=0:
    return True
  return False

def participates_in_org(user_username, org_username):
  cursor = cnx.cursor()
  cursor.execute("""INSERT INTO Users_Organizations (user_username, org_username)
                    VALUES (%s, %s)""", (user_username, org_username))
  cnx.commit()
  cursor.close()

def users_in_organization(org_username):
  cursor = cnx.cursor()
  cursor.execute("""SELECT first_name, last_name
                    FROM Users, Users_Organizations
                    WHERE Users_Organizations.org_username=%s AND Users.username = Users_Organizations.user_username""", (org_username,))
  return cursor.fetchall()

def organizations_user_is_in(user_username):
  cursor = cnx.cursor()
  cursor.execute("""SELECT Organizations.name
                    FROM Organizations, Users_Organizations
                    WHERE Users_Organizations.user_username=%s AND Organizations.username = Users_Organizations.org_username""", (user_username,))
  return cursor.fetchall()

def events_created_by_org(org_username):
  cursor = cnx.cursor()
  cursor.execute("SELECT name FROM Creates_Events WHERE org_username=%s", (org_username,))
  return cursor.fetchall()

def find_user(username):
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT first_name, last_name FROM Users WHERE username=%s", (username,))
    return cursor.fetchone()
  except mysql.connector.Error as err:
    return None

def find_organization(username):
  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT name FROM Organizations WHERE username=%s", (username,))
    return cursor.fetchone()
  except mysql.connector.Error as err:
    return None

def get_users_invites(user_username):
  cursor = cnx.cursor()
  cursor.execute("""SELECT Creates_Events.name
                    FROM Creates_Events, Invitations
                    WHERE Invitations.user_username=%s AND Invitations.eid = Creates_Events.eid""", (user_username,))
  return cursor.fetchall()

def get_events_in_category(category):
  cursor = cnx.cursor()
  cursor.execute("""SELECT Creates_Events.name
                    FROM Creates_Events, Events_Categories
                    WHERE Events_Categories.name=%s AND Creates_Events.eid = Events_Categories.eid""", (category,))
  return cursor.fetchall()

def user_past_events(user_username):
  present = datetime.now()
  present_time = present.time()
  present_date = present.date()
  cursor = cnx.cursor()
  cursor.execute("""SELECT DISTINCT *
                    FROM Creates_Events, Invitations
                    WHERE Invitations.user_username=%s AND Invitations.status_id=1
                          AND Creates_Events.eid = Invitations.eid AND ((SELECT DATEDIFF(%s, Creates_Events.date)) > 0
                          OR (SELECT DATEDIFF(%s, Creates_Events.date)) = 0 AND (SELECT TIMEDIFF(%s, Creates_Events.end_time)) > 0)""",
                (user_username, present_date, present_date, present_time))
  return cursor.fetchall()

def user_future_events(user_username):
  cursor = cnx.cursor()
  present = datetime.now()
  present_date = present.date()
  present_time = present.time()
  cursor.execute("""SELECT DISTINCT *
                    FROM Creates_Events, Invitations
                    WHERE Invitations.user_username=%s AND Invitations.status_id=1
                          AND Creates_Events.eid = Invitations.eid AND ((SELECT DATEDIFF(%s, Creates_Events.date)) < 0
                          OR (SELECT DATEDIFF(%s, Creates_Events.date)) = 0 AND (SELECT TIMEDIFF(%s, Creates_Events.start_time)) > 0)""",
                (user_username, present_date, present_date, present_time))
  return cursor.fetchall()


if __name__ == '__main__':
  #query = "SELECT username FROM Users WHERE username=%s"
  #cursor.execute(query, ('mengdilin',))
  #print cursor.fetchall()
  #name="test_event5"
  #date="2015-10-10"
  #start_time="00:00:01"
  #end_time="00:00:02"
  #description="hello"
  #image=None
  #org_name="broomclub"
  #building=None
  #room=None
  #print create_event(name, date, start_time, end_time, description, image, org_name, building, room)
  #print organization_login("broomclub", "broomslife "):
  #print create_event("test_event_2", "2015-10-13", "00:00:03", "00:00:23", "hello3", None, "org_3", "Math", 303)
  #print find_eid("test_event_3", "2015-10-13", "00:00:03", "00:00:23", "org_3", "Math", 303)
  #print user_past_events("test_last_14")
  print events_at_same_time("test_event_1", "2015-10-11", "00:00:01", "00:00:21", "org_1", "IAB", 101)

