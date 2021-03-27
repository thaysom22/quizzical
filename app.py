import os
from flask import (
    Flask, render_template, redirect,
    request, session, url_for, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import (
    generate_password_hash, check_password_hash)
# will not import env when running on cloud platform
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") 
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# default route for app
@app.route("/")
@app.route("/index")  
def default():
    """
    docstring here
    """
    loggedIn = 'user' in session  # check in cookies if user is logged in
    if loggedIn == False:
        return redirect(url_for("landing_page"))
    else:
        # get data from db
        # pass username to discover_page view
        return redirect(url_for("discover_page"))

@app.route("/landing")
def landing_page():
    """
    docstring here
    """
    loggedIn = 'user' in session
    return render_template("pages/landing.html",
        loggedIn=loggedIn)

@app.route("/discover")
def discover_page():
    """
    docstring here
    """
    loggedIn = 'user' in session
    return render_template("pages/discover.html",
        loggedIn=loggedIn)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True  # update to False prior to cloud deployment
    )