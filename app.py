from flask import Flask
from flask import session,render_template,url_for,redirect,request
import database

app = Flask(__name__)
app.secret_key="secret key" # Since we'll be using sessions

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('identify'))
    return redirect(url_for("about", data=["user is logged in"]))

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
      session["user"]=request.form['login_username']
          #username=request.form['username']
          #utils.add_user(username)
          #session["user"]=username
      print request.form['login_username']
      return redirect(url_for("user_dashboard"))

@app.route('/userdash', methods=['GET', 'POST'])
def user_dashboard():
  if request.method=="GET":
    return render_template('dash.html')
  if request.method=="POST":
    return render_template('dash.html')

@app.route('/orgdash', methods=['GET', 'POST'])
def org_dashboard():
  if request.method=="GET":
    return render_template('dash.html')
  if request.method=="POST":
    return render_template('dash.html')

@app.route('/orglogin',methods=['GET','POST'])
def org_login():
    if request.method=="GET":
      return render_template('login.html', incorrect=False, action_name="orglogin", sign_up_redir="/orgsignup")
    elif request.method=="POST":
      session["user"]=request.form['login_username']
          #username=request.form['username']
          #utils.add_user(username)
          #session["user"]=username
      print request.form['login_username']
      return redirect(url_for("org_login"))

@app.route('/orgsignup',methods=['GET','POST'])
def org_sign_up():
  if request.method=="GET":
    return render_template('signup.html', incorrect=False, user=False, action_name="orgsignup")
  elif request.method=="POST":
    print "org sign up"

@app.route('/usersignup',methods=['GET','POST'])
def user_sign_up():
  if request.method=="GET":
    return render_template('signup.html', incorrect=False, user=True, action_name="usersignup")
  elif request.method=="POST":
    print "user sign up"
    return redirect(url_for("userdash"))

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
