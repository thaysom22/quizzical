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
    loggedIn = 'user' in session  # check in session dict if user is logged in
    if not loggedIn:
        return redirect(url_for("landing"))
   
    # get data from db
    # pass username to discover_page view
    return redirect(url_for("discover"))

@app.route("/landing")
def landing():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if loggedIn:
        return redirect(url_for("discover"))

    return render_template("pages/landing.html")

@app.route("/discover")
def discover():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        return redirect(url_for("landing"))

    return render_template("pages/discover.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if loggedIn:
        username = session["user"]  # get user_id from session dict and pass to redirect function
        return redirect(url_for("profile"))
    
    if request.method == "GET":
        return render_template("pages/login.html")

    username_form = request.form.get("username").lower()  # get username from form (case-sensitive)
    existing_user = mongo.db.users.find_one(
        {"username": username_form})  # get user document from db (returns None if not found in db)
    
    if not existing_user:
        flash("Incorrect Username and/or Password")  # notify user of failure
        return redirect(url_for("login"))

    password_form = request.form.get("password")  # get password from form (not case-sensitive)
    correct_password = check_password_hash(existing_user["password"], password_form)

    if not correct_password:
        flash("Incorrect Username and/or Password")  # notify user of failure
        return redirect(url_for("login")) 

    username = existing_user["username"]
    session["user"] = username  # add to session dict 
    flash(f"Welcome back to Quizzical, {username}") #  flash message to newly logged in user on discover page
    
    return redirect(url_for("discover"))  # redirect to discover if login successful

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if loggedIn:
        flash("Logout first to register a new account")
        redirect(url_for("profile"))  # if logged in redirect to profile page

    if request.method == "GET":
        return render_template("pages/register.html")

    username_form = request.form.get("username").lower()  # form input validation done client-side
    existing_user = mongo.db.users.find_one(
        {"username": username_form})
    
    if existing_user:
        flash(f"The username: '{existing_user["username"]}' already exists")
        return redirect(url_for("register"))

    password_form = request.form.get("password")
    password_hash = generate_password_hash(
        password_form,
        method='pbkdf2:sha512',
        salt_length=12)
    
    new_user = {
        "username": username_form,
        "password": password_hash
    }

    mongo.db.users.insert_one(new_user)  # insert new user as document in db.users 
    session["user"] = username_form  # add to session dict 
    flash(f"Welcome to Quizzical, {username_form}") 
    
    return redirect(url_for("discover"))

# receives user_id as param or gets it from session dict
@app.route("/profile")
def profile():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to view your profile")
        return redirect(url_for("login"))
    
    username = session["user"]["username"]

    return render_template("pages/profile.html", username)


### START APP ###
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG") == "True"
    )