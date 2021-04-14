import os
from flask import (
    Flask, render_template, redirect,
    request, session, url_for, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import (
    generate_password_hash, check_password_hash)
from helpers import ObjectIdHelper 
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
    loggedIn = 'user' in session  # check in session dict
    if not loggedIn:
        return redirect(url_for("landing"))

    return redirect(url_for("discover"))


@app.route("/landing")
def landing():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if loggedIn:
        return redirect(url_for("discover"))

    return render_template("pages/landing.html", loggedIn=loggedIn)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if loggedIn:
        return redirect(url_for("profile"))
    
    if request.method == "GET":
        return render_template("pages/login.html", loggedIn=loggedIn)

    username_form = request.form.get("username").lower()  # get username from form (case-sensitive)
    existing_user = mongo.db.users.find_one(
        {"username": username_form})  # get user document from db (returns dict or None )
    
    if not existing_user:
        flash("Incorrect Username and/or Password")  # notify user of failure
        return redirect(url_for("login"))

    password_form = request.form.get("password")  # get password from form (not case-sensitive)
    correct_password = check_password_hash(
        existing_user["password"], password_form)

    if not correct_password:
        flash("Incorrect Username and/or Password")  # notify user of failure
        return redirect(url_for("login")) 

    # use existing_user dict to get category and age_range names from respective collections
    user_category_name = db.categories.find_one(
        {"_id": existing_user["user_category"]}
    )
    user_age_range_name = db.age_ranges.find_one(
        {"_id": existing_user["user_age_range"]}
    )
    
    # convert ObjectId types to string types before adding to session
    for k,v in existing_user.items():
        existing_user[k] = ObjectIdHelper.fromObjectId(v)

    # add name strings to existing_user dict before storing in session
    existing_user["user_category_name"] = user_category_name.category_name
    existing_user["user_age_range_name"] = user_age_range_name.age_range
    session["user"] = existing_user  # add existing_user dict to session object 
    flash(f"Welcome back to Quizzical, {username_form}") #  flash message to newly logged in user on discover page
    
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
        # read from categories and age_ranges collections in db
        all_categories = list(mongo.db.categories
            .find()
            .sort("category_name", 1))
        all_age_ranges = list(mongo.db.age_ranges
            .find()
            .sort("order", 1)) 

        # convert ObjectId values to strings
        for category in all_categories:
            category["_id"] = ObjectIdHelper.fromObjectId(category["_id"])

        for age_range in all_age_ranges:
            age_range["_id"] = ObjectIdHelper.fromObjectId(age_range["_id"])

        return render_template(
            "pages/register.html", 
            loggedIn=loggedIn, 
            all_categories=all_categories,
            all_age_ranges=all_age_ranges)

    # if request.method == "POST":
    username_form = request.form.get("username").lower()  # form input validation done client-side
    existing_user = mongo.db.users.find_one(
        {"username": username_form})
    
    if existing_user:
        flash(f"The username {username_form} already exists")
        return redirect(url_for("register"))

    # generate password hash from user password input
    password_form = request.form.get("password")
    password_hash = generate_password_hash(
        password_form,
        method='pbkdf2:sha512',
        salt_length=12)

    # get user category and age range ids from form as strings
    category_form_id = request.form.get("main_category")
    age_range_form_id = request.form.get("main_age_range")

    # convert ids to ObjectId type and insert in users collection
    new_user_db = {
        "username": username_form,
        "password": password_hash,
        "user_category": ObjectIdHelper.toObjectId(category_form_id),  
        "user_age_range": ObjectIdHelper.toObjectId(age_range_form_id)  
    }

    insert_new_user_result = mongo.db.users.insert_one(new_user_db)
    if not insert_new_user_result:
        flash("Could not register account, please try again later.")
        return redirect(url_for("register"))
    
    # get category and age_range names from db by id
    user_category_name = db.categories.find_one(
        {"_id": new_user_db["user_category"]}
    )
    user_age_range_name = db.age_ranges.find_one(
        {"_id": new_user_db["user_age_range"]}
    )

    # add user to session including inserted document ObjectId
    session["user"] = {
        "user_id": ObjectIdHelper.fromObjectId(
            insert_new_user_result.inserted_id),
        "username": username_form,
        "user_category_id": category_form_id,  
        "user_category_name": user_category_name.category_name,
        "user_age_range_id": age_range_form_id,
        "user_age_range_name": user_age_range_name.age_range  
    } 
    
    flash(f"Welcome to Quizzical, {username_form}") 
    
    return redirect(url_for("discover"))


@app.route("/discover", methods=["GET", "POST"])
def discover():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        return redirect(url_for("landing"))
    
    if request.method == "GET":
        # read all categories and all age_ranges from db
        all_categories = list(mongo.db.categories
            .find()
            .sort("category_name", 1))
        all_age_ranges = list(mongo.db.age_ranges
            .find()
            .sort("order", 1))

        user = session["user"]  # get data from session object
        username = user.get("username")
        user_category_id = ObjectIdHelper.toObjectId(user.get("user_category"))
        user_age_range_id = ObjectIdHelper.toObjectId(user.get("user_age_range"))
        

        # query quizzes collection for matches by category and age range



        return render_template("pages/discover.html", 
            loggedIn=loggedIn, 
            username=username, 
            all_categories=all_categories, 
            all_age_ranges=all_age_ranges)
        

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

    return render_template(
        "pages/profile.html",
        username=username,
        loggedIn=loggedIn)


### START APP ###
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG") == "True"
    )