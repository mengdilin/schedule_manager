from flask import Flask
from flask import session,render_template,url_for,redirect,request
import database
import datetime
import json
import uuid
import os

app = Flask(__name__)
app.secret_key="secret key" # Since we'll be using sessions
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

#format: '%Y-%m-%d'
def validate(date_text, date_format):
  try:
    datetime.datetime.strptime(date_text, date_format)
    return True
  except ValueError:
    return False

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
  if request.method=="GET":
    return render_template('dash.html', user_first=str(name[0]))
  if request.method=="POST":
    return render_template('dash.html', user_first=str(name[0]))

@app.route('/orgdash', methods=['GET', 'POST'])
def org_dashboard():
  user = session["user"]
  name = database.find_organization(user)
  if request.method=="GET":
    return render_template('dash.html', user_first=str(name[0]))
  if request.method=="POST":
    return render_template('dash.html', user_first=str(name[0]), nav_redir="/create_event", redir_name="Create Events")

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
    return render_template("event_form.html", locations=locations, categories=categories)
  if request.method=="POST":
    print "here"
    filePath = request.form['filePath']
    print "here1"
    name = request.form["name"]
    print "here2"
    description = request.form["description"]
    print "here3"
    date = request.form["date"]
    print "here4"
    start_time = request.form["start_time"]
    print "here5"
    end_time = request.form["end_time"]
    print "here6"
    location = request.form["location_hid"]
    print "here7"
    category = request.form["category_hid"]
    print "here8"
    org_name = database.find_organization(user)
    locations = location.split(" ")
    building = locations[0]
    room = location[1]
    print locations
    print database.create_event(name, date, start_time, end_time, None, None, org_name, None, None)
    print filePath, name, description, date, start_time, end_time, location, category
    return redirect(url_for("about"))


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
