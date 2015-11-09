from flask import Flask
from flask import send_from_directory
from flask import session,render_template,url_for,redirect,request
import database
import datetime
import json
import uuid
import os
import time

#left to do: populate dash board with actual data
#data need to lead to event's detail's page properly
# user needs to be able to participate in organization
app = Flask(__name__)
app.secret_key="secret key" # Since we'll be using sessions
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

def validate(date_text, date_format):
  try:
    datetime.datetime.strptime(date_text, date_format)
    return True
  except ValueError:
    return False

def parse_date(date_text):
  dates = date_text.split('-')
  return datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))

def parse_time(time_text):
  times = time_text.split(':')
  return datetime.time(int(times[0]),int(times[1]),int(times[2]))

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('identify'))
    return redirect(url_for("user_dashboard"))

@app.route('/identify',methods=['GET','POST'])
def identify():
  if request.method=="GET":
    return render_template('identify.html')
  elif request.method=="POST":
    if request.form['button']=='user':
      return redirect(url_for("user_login"))
    elif request.form['button'] == 'organization':
      return redirect(url_for("org_login"))

@app.route('/userlogin',methods=['GET','POST'])
def user_login():
    if request.method=="GET":
      return render_template('login.html', incorrect=False, action_name="userlogin", sign_up_redir="/usersignup")
    elif request.method=="POST":
      if database.user_login(request.form['login_username'], request.form['login_password']):
        session["user"]=request.form['login_username']
        return redirect(url_for("user_dashboard"))
      else:
        return render_template('login.html', incorrect=True, action_name="userlogin", sign_up_redir="/usersignup")

@app.route('/userdash', methods=['GET', 'POST'])
def user_dashboard():
  user = session["user"]
  name = database.find_user(user)
  user_invites_header = ["event id", "event name", "organizer", "date", "location"]
  invites_data = database.future_events_with_status(user, 3)
  events_data = database.user_future_events(user)
  past_events = database.user_past_events(user)
  if request.method=="GET":
    return render_template(
      'dash.html',
      user_first=str(name[0]),
      invites_table = "Received Invites",
      invites_table_header=user_invites_header,
      invites_table_data=invites_data,
      event_redir="/user_display_event_read/",
      invite_redir="/user_display_event/",
      events_table = "Upcoming Events",
      events_table_header= user_invites_header,
      events_table_data= events_data,
      search_redir="/userdash",
      past_events_table = "Past Events Attended",
      past_events_table_header = user_invites_header,
      past_events_table_data = past_events)
  if request.method=="POST":
    query = request.form["query"]
    if query != "":
      try:
        events_data = database.user_invites_by_category(user, request.form["query"])
      except:
        print "invalid query"
    return render_template(
      'dash.html',
      user_first=str(name[0]),
      invites_table = "Received Invites",
      invites_table_header=user_invites_header,
      invites_table_data=invites_data,
      event_redir="/user_display_event_read/",
      invite_redir="/user_display_event/",
      events_table = "Upcoming Events",
      events_table_header= user_invites_header,
      events_table_data= events_data,
      search_redir="/userdash",
      past_events_table = "Past Events Attended",
      past_events_table_header = user_invites_header,
      past_events_table_data = past_events)

@app.route('/orgdash', methods=['GET', 'POST'])
def org_dashboard():
  user = session["user"]
  name = database.find_organization(user)
  events_header = ["id", "name", "date", "building", "room"]
  invites_header = ["id", "name", "user"]
  invites_data = database.all_org_invites(user)
  events_data = database.events_created_by_org(user)
  if request.method=="GET":
    return render_template(
      'dash.html',
      user_first=str(name),
      nav_redir="/create_event",
      redir_name="Create Events",
      invites_table = "Upcoming Events' Invites",
      invites_table_header = invites_header,
      invites_table_data = invites_data,
      events_table = "Events Created by Me",
      events_table_header = events_header,
      events_table_data = events_data,
      invite_redir="/org_display_event/",
      event_redir="/org_display_event/")
  if request.method=="POST":
    query = request.form["query"]
    if query != "":
      try:
        events_data = database.org_events_by_category(user, request.form["query"])
      except:
        print "invalid query"
    return render_template(
      'dash.html',
      user_first=str(name),
      nav_redir="/create_event",
      redir_name="Create Events",
      invites_table = "Upcoming Events' Invites",
      invites_table_header = invites_header,
      invites_table_data = invites_data,
      events_table = "Events Created by Me",
      events_table_header = events_header,
      events_table_data = events_data,
      invite_redir="/org_display_event/",
      event_redir="/org_display_event/")

@app.route('/orglogin',methods=['GET','POST'])
def org_login():
  if request.method=="GET":
    return render_template('login.html', incorrect=False, action_name="orglogin", sign_up_redir="/orgsignup")
  elif request.method=="POST":
    if database.organization_login(request.form['login_username'], request.form['login_password']):
      session["user"]=request.form['login_username']
      return redirect(url_for("org_dashboard"))
    else:
      return render_template('login.html', incorrect=True, action_name="orglogin", sign_up_redir="/orgsignup")

@app.route('/create_event',methods=['GET','POST'])
def create_event():
  user = session['user']
  locations = database.get_locations()
  categories = database.get_categories()
  if request.method=="GET":
    return render_template("event_form.html", locations=locations, categories=categories, incorrect=False, dash_redir='/orgdash')
  if request.method=="POST":
    try:
      filePath = request.form['filePath']
      name = request.form["name"]
      description = request.form["description"]
      date = request.form["date"]
      start_time = request.form["start_time"]
      end_time = request.form["end_time"]
      location = request.form["location_hid"]
      category = request.form["category_hid"]
      building = None
      room = None
      if location is not None:
        locations_tmp = location.split(" ")
        building = locations_tmp[0]
        room = locations_tmp[1]
      result = database.create_event(name,
        parse_date(date),
        parse_time(start_time),
        parse_time(end_time),
        description,
        filePath,
        user,
        building,
        room)
      if result != False:
        database.create_event_category(result, category)
        return redirect(url_for("org_display_event", eid=int(result)))
      else:
        return render_template("event_form.html", locations=locations, categories=categories, incorrect=True, dash_redir='/orgdash')
    except:
      return render_template("event_form.html", locations=locations, categories=categories, incorrect=True, dash_redir='/orgdash')

@app.route('/org_display_event/<int:eid>',methods=['GET', 'POST'])
def org_display_event(eid):
  event = database.find_event(eid)
  category = database.get_categories_of_event(eid)
  if request.method=='GET':
    return render_template("event.html",
      name=event[0],
      filepath=event[5],
      description=event[4],
      date=event[1],
      start_time=event[2],
      end_time=event[3],
      location=event[7]+" "+event[8],
      category=str(category),
      organizer=event[6],
      event=True,
      incorrect=False,
      success=False,
      eid=eid,
      dash_redir='/orgdash')
  if request.method=='POST':
    username=request.form["name"]
    if database.create_invitation(username, session["user"], eid):
      return render_template("event.html",
      name=event[0],
      filepath=event[5],
      description=event[4],
      date=event[1],
      start_time=event[2],
      end_time=event[3],
      location=event[7]+" "+event[8],
      category=str(category),
      organizer=event[6],
      event=True,
      incorrect=False,
      success=True,
      eid=eid,
      dash_redir='/orgdash')
    else:
      return render_template("event.html",
      name=event[0],
      filepath=event[5],
      description=event[4],
      date=event[1],
      start_time=event[2],
      end_time=event[3],
      location=event[7]+" "+event[8],
      category=str(category),
      organizer=event[6],
      event=True,
      incorrect=True,
      success=False,
      eid=eid,
      dash_redir='/orgdash')

@app.route('/user_display_event/<int:eid>',methods=['GET', 'POST'])
def user_display_event(eid):
  event = database.find_event(eid)
  category = database.get_categories_of_event(eid)
  if request.method=='GET':
    return render_template("event.html",
      name=event[0],
      filepath=event[5],
      description=event[4],
      date=event[1],
      start_time=event[2],
      end_time=event[3],
      location=event[7]+" "+event[8],
      category=str(category),
      organizer=event[6],
      event=False,
      incorrect=False,
      success=False,
      eid=eid,
      dash_redir='/userdash',
      user_decide=True)
  if request.method=='POST':
    value = request.form["invite"]
    status_id = 3
    if value == "Accept":
      status_id = 1
    elif value == "Decline":
      status_id = 2
    if status_id == 1 or status_id == 2:
      database.update_invite(session["user"], event[6], eid, status_id)
      return redirect(url_for("user_dashboard"))
    if value == "Participate":
      org_username = request.form["name"]
      success = database.participates_in_org(session["user"], org_username)
      print success
      return render_template("event.html",
        name=event[0],
        filepath=event[5],
        description=event[4],
        date=event[1],
        start_time=event[2],
        end_time=event[3],
        location=event[7]+" "+event[8],
        category=str(category),
        organizer=event[6],
        event=False,
        incorrect=(not success),
        success=success,
        eid=eid,
        dash_redir='/userdash',
        user_decide=True)

@app.route('/user_display_event_read/<int:eid>', methods=['GET'])
def user_display_event_read(eid):
  event = database.find_event(eid)
  category = database.get_categories_of_event(eid)
  if request.method=='GET':
    return render_template("event.html",
      name=event[0],
      filepath=event[5],
      description=event[4],
      date=event[1],
      start_time=event[2],
      end_time=event[3],
      location=event[7]+" "+event[8],
      category=str(category),
      organizer=event[6],
      event=False,
      incorrect=False,
      success=False,
      eid=eid,
      dash_redir='/userdash',
      user_decide=False)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  print send_from_directory(app.config['UPLOAD_FOLDER'],filename)
  return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/orgsignup',methods=['GET','POST'])
def org_sign_up():
  if request.method=="GET":
    return render_template('signup.html', incorrect=False, user=False, action_name="orgsignup")
  elif request.method=="POST":
    username = request.form["username"]
    password = request.form["password"]
    confirm_pass = request.form["confirm"]
    name = request.form["org_name"]
    if password != confirm_pass or not database.create_organization(name, username, password):
      return render_template('signup.html', incorrect=True, user=False, action_name="orgsignup")
    else:
      return redirect(url_for("org_dashboard"))

@app.route('/usersignup',methods=['GET','POST'])
def user_sign_up():
  if request.method=="GET":
    return render_template('signup.html', incorrect=False, user=True, action_name="usersignup")
  elif request.method=="POST":
    username = request.form["username"]
    password = request.form["password"]
    confirm_pass = request.form["confirm"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    if password != confirm_pass or not database.create_user(first_name, last_name, username, password):
      return render_template('signup.html', incorrect=True, user=True, action_name="usersignup")
    else:
      return redirect(url_for("user_dashboard"))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    file = request.files['file']
    extension = os.path.splitext(file.filename)[1]
    f_name = str(uuid.uuid4()) + extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    return json.dumps({'filename':f_name})

@app.route('/about')
def about():
  return render_template('index.html', data=['log in user'])

@app.route("/logout")
def logout():
  session.pop('user')
  return redirect(url_for('identify'))

if __name__=="__main__":
  app.debug=True
  app.run()
