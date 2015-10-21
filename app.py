from flask import Flask
from flask import session,render_template,url_for,redirect,request
import database

app = Flask(__name__)
app.secret_key="secret key" # Since we'll be using sessions

@app.route("/")
def index():
  return render_template('index.html', data=database.execute_query(("SELECT * FROM Users")))

if __name__=="__main__":
  app.debug=True
  app.run()
