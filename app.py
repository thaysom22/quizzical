import os
from flask import (
    Flask, render_template, redirect,
    request, session, url_for, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import (
    generate_password_hash, check_password_hash)
from helpers import ObjectIdHelper
from random import sample
# will not import env.py when running on cloud platform
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") 
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)


### DEFAULT ROUTE ###

@app.route("/")
@app.route("/index")  
def default():
    """
    Check if user is logged in and return redirect
    to welcome or discover template
    """
    loggedIn = 'user' in session 
    if not loggedIn:
        return redirect(url_for("welcome", _external=True, _scheme='https'))

    return redirect(url_for("discover", _external=True, _scheme='https'))


### WELCOME PAGE ###

@app.route("/welcome")
def welcome():
    """
    Return render_template for welcome template
    or redirect to discover if user logged in
    """
    loggedIn = 'user' in session
    if loggedIn:
        return redirect(url_for("discover", _external=True, _scheme='https'))

    return render_template(
        "pages/welcome.html",
        loggedIn=loggedIn,
        active_page="Welcome"
    )


### LOGIN AND LOGOUT ###

# LOGIN #

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    If GET request: return render_template for 
    discover template.
    If POST request: read form
    data and check mongodb collections: return
    redirect to login page if username not
    found and/or password does not match; else update
    found user document and add to session dict
    as value for 'user' key, then return redirect to
    discover
    """
    loggedIn = 'user' in session
    if loggedIn:
        return redirect(url_for("discover", _external=True, _scheme='https'))

    # GET #    
    if request.method == "GET":
        return render_template(
            "pages/login.html", 
            loggedIn=loggedIn,
            active_page="Login"
        )

    # POST #
    username_form = request.form.get("username").lower()  # (case-sensitive)
    existing_user = mongo.db.users.find_one(
        {
            "username": username_form
        }
    )
    if not existing_user:
        flash("Incorrect username and/or password", "not-auth")  
        
        return redirect(url_for("login", _external=True, _scheme='https'))

    password_form = request.form.get("password") 
    correct_password = check_password_hash(
        existing_user["password"], password_form)

    if not correct_password:
        flash("Incorrect username and/or password", "not-auth")  
        
        return redirect(url_for("login", _external=True, _scheme='https')) 

    # use existing_user dict to get category and age_range data
    user_category_data = mongo.db.categories.find_one(
        {
            "_id": existing_user["user_category_id"]
        }
    )
    user_age_range_data = mongo.db.age_ranges.find_one(
        {
            "_id": existing_user["user_age_range_id"]
        }
    )
    # convert ObjectId types to string types before adding to session
    for k, v in existing_user.items():
        existing_user[k] = ObjectIdHelper.fromObjectId(v)

    # add name strings to existing_user dict before storing in session
    existing_user["user_category_name"] = user_category_data["category_name"]
    existing_user["user_age_range_name"] = user_age_range_data["age_range"]
    session["user"] = existing_user  
    flash(f"Welcome back to Quizzical, {username_form}", "success") 
    
    return redirect(url_for("discover", _external=True, _scheme='https'))


# LOGOUT #

@app.route("/logout")
def logout():
    """
    If user logged in: remove 'user' from session
    dict. Return redirect to discover.
    """
    loggedIn = 'user' in session
    if not loggedIn:
        return redirect(url_for("login", _external=True, _scheme='https'))  

    username = session.get("user").get("username")
    session.pop("user")
    flash(f"{username} has been logged out.", "success")
    
    return redirect(url_for("login", _external=True, _scheme='https'))


### REGISTER ###

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    If GET request: read all category and age range
    names from mongodb, return render_template for 
    register template. If POST request: read form data, 
    check mongodb that no document with same username field 
    value exists, hash user password, add user document 
    to mongodb and to session dict as value for 'user'
    key, finally, redirect to discover.
    """
    loggedIn = 'user' in session
    if loggedIn:
        flash(
            "Logout first to register a new account", 
            "invalid-action"
        )
        return redirect(url_for("discover", _external=True, _scheme='https'))

    # GET #
    if request.method == "GET":
        # read from categories and age_ranges collections in db
        all_categories = list(
            mongo.db.categories.find(sort=[("category_name", 1)])
        )
        all_age_ranges = list(
            mongo.db.age_ranges.find(sort=[("order", 1)])
        )
        # convert ObjectId values to strings
        for category in all_categories:
            category["_id"] = ObjectIdHelper.fromObjectId(category["_id"])

        for age_range in all_age_ranges:
            age_range["_id"] = ObjectIdHelper.fromObjectId(age_range["_id"])

        return render_template(
            "pages/register.html", 
            loggedIn=loggedIn,
            active_page="Register", 
            all_categories=all_categories,
            all_age_ranges=all_age_ranges)

    # POST #
    username_form = request.form.get("username").lower()  # form input validation done client-side
    existing_user = mongo.db.users.find_one(
        {
            "username": username_form
        }
    )
    if existing_user:
        flash(
            f"The username {username_form} already exists",
            "not-auth"
        )
        return redirect(url_for("register", _external=True, _scheme='https'))

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
        "user_category_id": ObjectIdHelper.toObjectId(category_form_id),  
        "user_age_range_id": ObjectIdHelper.toObjectId(age_range_form_id)  
    }
    insert_new_user_result = mongo.db.users.insert_one(new_user_db)
    if not insert_new_user_result:
        flash(
            "Could not register account, please try again later.",
            "error"
        )
        return redirect(url_for("register", _external=True, _scheme='https'))
    
    # get category and age_range documents from db by id
    user_category = mongo.db.categories.find_one(
        {
            "_id": new_user_db["user_category_id"]
        }
    )
    user_age_range = mongo.db.age_ranges.find_one(
        {
            "_id": new_user_db["user_age_range_id"]
        }
    )

    # add user to session including inserted document ObjectId...
    # include category name and age range name
    session["user"] = {
        "_id": ObjectIdHelper.fromObjectId(
            insert_new_user_result.inserted_id),
        "username": username_form,
        "user_category_id": category_form_id,  
        "user_category_name": user_category.get("category_name"),
        "user_age_range_id": age_range_form_id,
        "user_age_range_name": user_age_range.get("age_range")  
    } 
    flash(f"Welcome to Quizzical, {username_form}", "success") 
    
    return redirect(url_for("discover", _external=True, _scheme='https'))



### DISCOVER ###

@app.route("/discover")
def discover():
    """
    Read all category names and all age range names from
    mongodb collections, read and organize data from mongodb 
    quizzes collection into dicts, read user data from session
    dict: combine to create reccommended quizzes dicts and limit to
    maximum of 3 quizzes by taking random sample. Return 
    render_template for discover template with dicts passed as
    arguments.
    """
    loggedIn = 'user' in session
    if not loggedIn:
        return redirect(url_for("welcome", _external=True, _scheme='https'))
    
    # read all categories and all age_ranges from db
    all_categories = list(
        mongo.db.categories.find(sort=[("category_name", 1)])
    )
    all_age_ranges = list(
        mongo.db.age_ranges.find(sort=[("order", 1)])
    )
    # read from quizzes collection by category
    # credit for "$arrayElemAt" workaround: https://stackoverflow.com/questions/37691727/how-to-use-mongodbs-aggregate-lookup-as-findone  
    quizzes_by_category = {}
    for category in all_categories:
        quizzes_by_category[category["_id"]] = list(mongo.db.quizzes.aggregate([
            { "$match": { "quiz_category_id": category["_id"] } },
            { "$sample": { "size": 3 } },
            { 
                "$lookup": {  
                    "from": "age_ranges",
                    "localField": "quiz_age_range_id",
                    "foreignField": "_id",
                    "as": "quiz_age_range_data"
                } 
            },
            { 
                "$lookup": {  
                    "from": "users",
                    "localField": "quiz_owner_id",
                    "foreignField": "_id",
                    "as": "quiz_owner_data"
                } 
            },
            { 
                "$addFields": {
                    "quiz_category_data": category,
                    # specifying an existing field name in an $addFields operation causes the original field to be replaced
                    "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                    "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]}
                }
            },  
            { 
                "$project": {
                    "questions": False,
                    "quiz_owner_data.password": False
                } 
            }
        ]))

    # read from quizzes collection by age_range
    quizzes_by_age_range = {}
    for age_range in all_age_ranges:
        quizzes_by_age_range[age_range["_id"]] = list(mongo.db.quizzes.aggregate([
            { "$match": {"quiz_age_range_id": age_range["_id"]} },
            { "$sample": { "size": 3 } },
            { 
                "$lookup": {  
                    "from": "categories",
                    "localField": "quiz_category_id",
                    "foreignField": "_id",
                    "as": "quiz_category_data"
                } 
            },
            { 
                "$lookup": {  
                    "from": "users",
                    "localField": "quiz_owner_id",
                    "foreignField": "_id",
                    "as": "quiz_owner_data"
                } 
            },
            { 
                "$addFields": {
                    "quiz_age_range_data": age_range,
                    "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                    "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]}
                } 
            },
            { 
                "$project": {
                    "questions": False,
                    "quiz_owner_data.password": False
                } 
            }
        ]))    
    
    user = session.get("user")  # get data from session object
    username = user.get("username")
    user_category_id = user.get("user_category_id")
    user_age_range_id = user.get("user_age_range_id")
    recc_quizzes_by_category = list(mongo.db.quizzes.aggregate([
        { "$match": {"quiz_category_id": ObjectIdHelper.toObjectId(user_category_id)} },
        { "$sample": { "size": 3 } },
        {   
            "$lookup": {
                "from": "categories",
                "localField": "quiz_category_id",
                "foreignField": "_id",
                "as": "quiz_category_data"
            }
        },
        {   
            "$lookup": {
                "from": "age_ranges",
                "localField": "quiz_age_range_id",
                "foreignField": "_id",
                "as": "quiz_age_range_data"
            }
        },
        { 
            "$lookup": {  
                "from": "users",
                "localField": "quiz_owner_id",
                "foreignField": "_id",
                "as": "quiz_owner_data"
            } 
        },
        { 
            "$addFields": {
                "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]}
            } 
        },
        { 
            "$project": {
                "questions": False,
                "quiz_owner_data.password": False
            } 
        }
    ]))
    
    recc_quizzes_by_age_range = list(mongo.db.quizzes.aggregate([
        { "$match": {"quiz_age_range_id": ObjectIdHelper.toObjectId(user_age_range_id)} },
        { "$sample": { "size": 3 } },
        {   
            "$lookup": {
                "from": "categories",
                "localField": "quiz_category_id",
                "foreignField": "_id",
                "as": "quiz_category_data"
            }
        },
        {   
            "$lookup": {
                "from": "age_ranges",
                "localField": "quiz_age_range_id",
                "foreignField": "_id",
                "as": "quiz_age_range_data"
            }
        },
        { 
            "$lookup": {  
                "from": "users",
                "localField": "quiz_owner_id",
                "foreignField": "_id",
                "as": "quiz_owner_data"
            } 
        },
        { 
            "$addFields": {
                "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]}
            } 
        },
        { 
            "$project": {
                "questions": False,
                "quiz_owner_data.password": False
            } 
        }
    ]))

    # create list of max 3 unique quizzes
    recc_quizzes = recc_quizzes_by_category + recc_quizzes_by_age_range
    # dict comp. to remove duplicates, CREDIT: https://www.geeksforgeeks.org/python-removing-duplicate-dicts-in-list/ 
    recc_quizzes = list({item["_id"]: item for item in recc_quizzes}.values())
    if len(recc_quizzes) > 3:
        recc_quizzes = sample(recc_quizzes, 3)   

    return render_template("pages/discover.html", 
        loggedIn=loggedIn,
        active_page="Discover", 
        username=username, 
        all_categories=all_categories, 
        all_age_ranges=all_age_ranges,
        user_category_id=user_category_id,
        user_age_range_id=user_age_range_id,
        quizzes_by_category=quizzes_by_category,
        quizzes_by_age_range=quizzes_by_age_range,
        recc_quizzes=recc_quizzes,
        search_query=""
    )
        

### SEARCH ###

@app.route("/search", methods=["GET", "POST"])
def search():
    """
    If GET request: read values from request.args and
    use values to determine query to send to mongodb to 
    read all quizzes, reccommended quizzes, quizzes by
    age range, quizzes by category; return redirect to
    discover if no valid url arguments are provided.
    If POST request: use search_query url parameter to 
    send a query to read quizzes using existing text index 
    on quizzes collection. 

    Return render_template for search template with documents
    returned from executed mongodb query passed as argument.
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to search quizzes", "not-auth")
        return redirect(url_for("login", _external=True, _scheme='https'))
       
    username = session.get("user").get("username") 
    # use request.args to parse optional url parameters...
    # CREDIT: https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask 
    request_args = request.args
    # GET #
    if request.method == "GET":
        all_quizzes = request_args.get('all_quizzes')
        recc = request_args.get('recc')
        category = request_args.get('category')
        age_range = request_args.get('age_range')
        search_query = None 
        if all_quizzes == "true":
            # match all documents in collection
            # CREDIT: https://stackoverflow.com/questions/59918113/mongodb-aggregate-match-a-document-or-all
            search_results = list(mongo.db.quizzes.aggregate([
                { 
                    "$match": {
                         "_id" : {"$exists": "True"}
                    }
                },
                {   
                    "$lookup": {
                        "from": "categories",
                        "localField": "quiz_category_id",
                        "foreignField": "_id",
                        "as": "quiz_category_data"
                    }
                },
                {   
                    "$lookup": {
                        "from": "age_ranges",
                        "localField": "quiz_age_range_id",
                        "foreignField": "_id",
                        "as": "quiz_age_range_data"
                    }
                },
                { 
                    "$lookup": {  
                        "from": "users",
                        "localField": "quiz_owner_id",
                        "foreignField": "_id",
                        "as": "quiz_owner_data"
                    } 
                },
                { 
                    "$addFields": {
                        "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                        "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                        "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
                        "num_questions": { "$size": "$questions" }
                    } 
                },
                { 
                    "$project": {
                        "questions": False,
                        "quiz_owner_data.password": False
                    } 
                },
                {
                    "$sort": {
                        "num_questions": -1 }
                }
            ]
        ))

        elif recc == "true":
            recc_quizzes_by_category = list(mongo.db.quizzes.aggregate([
                { 
                    "$match": {
                        "quiz_category_id": ObjectIdHelper.toObjectId(category)
                    }
                },
                {   
                    "$lookup": {
                        "from": "categories",
                        "localField": "quiz_category_id",
                        "foreignField": "_id",
                        "as": "quiz_category_data"
                    }
                },
                {   
                    "$lookup": {
                        "from": "age_ranges",
                        "localField": "quiz_age_range_id",
                        "foreignField": "_id",
                        "as": "quiz_age_range_data"
                    }
                },
                { 
                    "$lookup": {  
                        "from": "users",
                        "localField": "quiz_owner_id",
                        "foreignField": "_id",
                        "as": "quiz_owner_data"
                    } 
                },
                { 
                    "$addFields": {
                        "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                        "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                        "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
                        "num_questions": { "$size": "$questions" }
                    } 
                },
                { 
                    "$project": {
                        "questions": False,
                        "quiz_owner_data.password": False
                    } 
                }
            ]))
            recc_quizzes_by_age_range = list(mongo.db.quizzes.aggregate([
                { 
                    "$match": {
                        "quiz_age_range_id": ObjectIdHelper.toObjectId(age_range)
                    } 
                },
                {   
                    "$lookup": {
                        "from": "categories",
                        "localField": "quiz_category_id",
                        "foreignField": "_id",
                        "as": "quiz_category_data"
                    }
                },
                {   
                    "$lookup": {
                        "from": "age_ranges",
                        "localField": "quiz_age_range_id",
                        "foreignField": "_id",
                        "as": "quiz_age_range_data"
                    }
                },
                { 
                    "$lookup": {  
                        "from": "users",
                        "localField": "quiz_owner_id",
                        "foreignField": "_id",
                        "as": "quiz_owner_data"
                    } 
                },
                { 
                    "$addFields": {
                        "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                        "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                        "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
                        "num_questions": { "$size": "$questions" }
                    } 
                },
                { 
                    "$project": {
                        "questions": False,
                        "quiz_owner_data.password": False
                    } 
                }
            ]))
            search_results = recc_quizzes_by_category + recc_quizzes_by_age_range
            search_results = list({item["_id"]: item for item in search_results}.values())  # remove duplicates

        elif category:
            search_results = list(mongo.db.quizzes.aggregate([
                { 
                    "$match": { 
                        "quiz_category_id": ObjectIdHelper.toObjectId(category) 
                    } 
                },
                { 
                    "$lookup": {  
                        "from": "age_ranges",
                        "localField": "quiz_age_range_id",
                        "foreignField": "_id",
                        "as": "quiz_age_range_data"
                    } 
                },
                { 
                    "$lookup": {  
                        "from": "users",
                        "localField": "quiz_owner_id",
                        "foreignField": "_id",
                        "as": "quiz_owner_data"
                    } 
                },
                { 
                    "$addFields": {
                        "quiz_category_data": category,
                        # specifying an existing field name in an $addFields operation causes the original field to be replaced
                        "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                        "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
                        "num_questions": { "$size": "$questions" }
                    }
                },  
                { 
                    "$project": {
                        "questions": False,
                        "quiz_owner_data.password": False
                    } 
                }
            ]))            
        
        elif age_range:
            search_results = list(mongo.db.quizzes.aggregate([
                { 
                    "$match": {
                        "quiz_age_range_id": ObjectIdHelper.toObjectId(age_range) 
                    } 
                },
                { 
                    "$lookup": {  
                        "from": "categories",
                        "localField": "quiz_category_id",
                        "foreignField": "_id",
                        "as": "quiz_category_data"
                    } 
                },
                { 
                    "$lookup": {  
                        "from": "users",
                        "localField": "quiz_owner_id",
                        "foreignField": "_id",
                        "as": "quiz_owner_data"
                    } 
                },
                { 
                    "$addFields": {
                        "quiz_age_range_data": age_range,
                        "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                        "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
                        "num_questions": { "$size": "$questions" }
                    } 
                },
                { 
                    "$project": {
                        "questions": False,
                        "quiz_owner_data.password": False
                    } 
                }
            ]))    
            
        else:
            # This is a GET request to /search endpoint...
            #  w/o any required url parameters
            return redirect(url_for("discover", _external=True, _scheme='https'))  

    # POST #
    if request.method == "POST":
        search_query = request.form.get('search_query').lower()
        # CREDIT for constructing search with text index: https://docs.mongodb.com/manual/text-search/
        search_results = list(mongo.db.quizzes.aggregate([
            { 
                "$match": {
                    "$text": { "$search": search_query }
                }
            },
            {   
                "$lookup": {
                    "from": "categories",
                    "localField": "quiz_category_id",
                    "foreignField": "_id",
                    "as": "quiz_category_data"
                }
            },
            {   
                "$lookup": {
                    "from": "age_ranges",
                    "localField": "quiz_age_range_id",
                    "foreignField": "_id",
                    "as": "quiz_age_range_data"
                }
            },
            { 
                "$lookup": {  
                    "from": "users",
                    "localField": "quiz_owner_id",
                    "foreignField": "_id",
                    "as": "quiz_owner_data"
                } 
            },
            { 
                "$addFields": {
                    "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                    "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                    "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
                    "num_questions": { "$size": "$questions" }
                } 
            },
            { 
                "$project": {
                    "questions": False,
                    "quiz_owner_data.password": False
                } 
            },
            {
                "$sort": {
                    "score": { "$meta": "textScore" }, "num_questions": -1 }
            }
        ]))
    # GET and POST #
    return render_template("pages/search.html",
        active_page="Search", 
        username=username,
        loggedIn=loggedIn,
        search_query=search_query,
        search_results=search_results,
        all_quizzes=all_quizzes
    )


### CREATE, READ, UPDATE, DELETE QUIZZES ###

# CREATE QUIZ #

@app.route("/create-quiz", methods=["GET", "POST"])
def create_quiz():
    """
    If GET request: read all category and age range names from
    mongodb, render_template for create-quiz template and pass
    category and age range names as arguments.
    If POST request: read form data from request into format of 
    quiz document, insert into mongodb quizzes collection: return
    redirect to add_question with inserted_id as argument 
    if successful, or redirect to create_quiz if not.
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes", "not-auth")
        return redirect(url_for("login", _external=True, _scheme='https'))

    # GET #
    if request.method == "GET":
        all_categories = list(
            mongo.db.categories.find(sort=[("category_name", 1)])
        )
        all_age_ranges = list(
            mongo.db.age_ranges.find(sort=[("order", 1)])
        )
        
        return render_template(
            "pages/create-quiz.html",
            active_page="Create Quiz", 
            loggedIn=loggedIn,
            all_categories=all_categories,
            all_age_ranges=all_age_ranges
        )

    # POST #
    insert_quiz_result = mongo.db.quizzes.insert_one(
        {
            "title": request.form.get('create_quiz_title'),
            "quiz_owner_id": ObjectIdHelper.toObjectId(session.get('user').get('_id')),
            "quiz_category_id": ObjectIdHelper.toObjectId(request.form.get('create_quiz_category')),  
            "quiz_age_range_id": ObjectIdHelper.toObjectId(request.form.get('create_quiz_age_range')),
            "questions": []  
        }
    )
    if not insert_quiz_result:
        flash("Quiz was not created. Try again later.", "error") 
        return redirect(url_for("create_quiz", _external=True, _scheme='https'))

    new_quiz_id = insert_quiz_result.inserted_id
    flash(f"{request.form.get('create_quiz_title')} has been created", "success")
        
    return redirect(url_for(
        "add_question", 
        quiz_id=new_quiz_id,
        create_quiz_process="true", 
        _external=True,
        _scheme='https'
    ))


# READ QUIZ #

@app.route("/view-quiz/<view_quiz_id>")
def view_quiz(view_quiz_id):
    """
    Read quiz document from mongodb quizzes collection by
    view_quiz_id and include data from other collections in 
    returned document (redirect to discover if not found), 
    check if user ID in session dict matches quiz_owner_id field,
    return render_template for view-quiz template passing quiz 
    data and user is owner boolean. 

    Parameters:
    view_quiz_id -- id for quiz document to be read and viewed
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to view quizzes", "not-auth")
        return redirect(url_for("login", _external=True, _scheme='https'))

    view_quiz_data = list(mongo.db.quizzes.aggregate([
        { 
            "$match": {
                "_id": ObjectIdHelper.toObjectId(view_quiz_id) 
            } 
        },
        { 
            "$lookup": {  
                "from": "questions",
                # localField quizzes.questions is an array...
                # $lookUp operation matches a document in questions coll for each element of arrray
                "localField": "questions",  
                "foreignField": "_id",
                "as": "questions_data"
            } 
        },
        {   
            "$lookup": {
                "from": "categories",
                "localField": "quiz_category_id",
                "foreignField": "_id",
                "as": "quiz_category_data"
            }
        },
        {   
            "$lookup": {
                "from": "age_ranges",
                "localField": "quiz_age_range_id",
                "foreignField": "_id",
                "as": "quiz_age_range_data"
            }
        },
        { 
            "$lookup": {  
                "from": "users",
                "localField": "quiz_owner_id",
                "foreignField": "_id",
                "as": "quiz_owner_data"
            } 
        },
        { 
            "$addFields": {
                "num_questions": { "$size": "$questions" },
                "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
        } 
        },
        { 
            "$project": {
                "quiz_owner_data.password": False
            } 
        }
    ]))

    if not view_quiz_data:
        flash('Error: quiz not found')
        return redirect(url_for('discover', _external=True, _scheme='https'))
    
    # view_quiz_data is a one-element list so access first element
    view_quiz_data = view_quiz_data[0]
    num_questions = view_quiz_data.get('num_questions')
    # view-quiz.html template needs to know if current user is owner of viewed quiz
    user_is_owner = (
        view_quiz_data.get('quiz_owner_id') == 
            ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )

    return render_template("pages/view-quiz.html",
            active_page="View Quiz",
            view_quiz_id=view_quiz_id, 
            user_is_owner=user_is_owner,
            view_quiz_data=view_quiz_data,
            num_questions=num_questions,
            loggedIn=loggedIn)


# UPDATE QUIZ #

@app.route("/edit-quiz/<edit_quiz_id>", methods=["GET", "POST"])
def edit_quiz(edit_quiz_id):
    """
    If GET request: read all category and age range names from
    mongodb, read quiz data from mongodb quizzes collection by
    edit_quiz_id and include data from other collections in returned
    document (redirect to discover if not found), check user id value
    in session dict matches user_owner_id filed value in document
    (if not redirect to view quiz), finally, return render_template 
    for edit-quiz template passing returned document from mongodb 
    as argument.

    If POST request: read form data from request and update 
    quiz document identified by edit_quiz_id in mongodb quizzes
    collection, return redirect to edit_quiz (same route) 
    passing edit_quiz_id as argument.

    Parameters:
    edit_quiz_id -- id for quiz document in mongodb to be updated
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to edit a quiz", "not-auth")
        return redirect(url_for("login", _external=True, _scheme='https'))

    # POST #
    if request.method == "POST":
        # input values have been validated client-side
        update_quiz_result = mongo.db.quizzes.update_one(
            { "_id": ObjectIdHelper.toObjectId(edit_quiz_id) },
            { 
                "$set": { 
                    "title": request.form.get('edit-title'),
                    "quiz_category_id": ObjectIdHelper.toObjectId(
                        request.form.get('edit-category')),
                    "quiz_age_range_id": ObjectIdHelper.toObjectId(
                        request.form.get('edit-age-range'))
                } 
            }
        )    
        # update successful guard clause
        if not update_quiz_result:
            flash("Quiz could not be updated. Try again later.", "error")
        else:
            flash("Quiz updated.", "success")

        # redirect to view quiz
        return redirect(url_for(
            'edit_quiz', 
            edit_quiz_id=edit_quiz_id,
            _external=True, 
            _scheme='https'
        ))

    # GET #
    # read all categories and all age_ranges from db
    all_categories = list(
        mongo.db.categories.find(sort=[("category_name", 1)])
    )
    all_age_ranges = list(
        mongo.db.age_ranges.find(sort=[("order", 1)])
    )
    edit_quiz_data = list(mongo.db.quizzes.aggregate([
        { 
            "$match": {
                "_id": ObjectIdHelper.toObjectId(edit_quiz_id) 
            } 
        },
        { 
            "$lookup": {  
                "from": "questions",
                "localField": "questions",  
                "foreignField": "_id",
                "as": "questions_data"
            } 
        },
        {   
            "$lookup": {
                "from": "categories",
                "localField": "quiz_category_id",
                "foreignField": "_id",
                "as": "quiz_category_data"
            }
        },
        {   
            "$lookup": {
                "from": "age_ranges",
                "localField": "quiz_age_range_id",
                "foreignField": "_id",
                "as": "quiz_age_range_data"
            }
        },
        { 
            "$lookup": {  
                "from": "users",
                "localField": "quiz_owner_id",
                "foreignField": "_id",
                "as": "quiz_owner_data"
            } 
        },
        { 
            "$addFields": {
                "num_questions": { "$size": "$questions" },
                "quiz_category_data": { "$arrayElemAt": [ "$quiz_category_data", 0 ]},
                "quiz_age_range_data": { "$arrayElemAt": [ "$quiz_age_range_data", 0 ]},
                "quiz_owner_data": { "$arrayElemAt": [ "$quiz_owner_data", 0 ]},
        } 
        },
        { 
            "$project": {
                "quiz_owner_data.password": False
            } 
        }
    ]))

    if not edit_quiz_data:
        flash('Cannot edit - quiz not found.', "error")
        return redirect(url_for('discover', _external=True, _scheme='https'))

    # check user is owner by reading from db with edit_quiz_id
    # edit_quiz_data is a one-element list so access first element
    edit_quiz_data = edit_quiz_data[0]
    num_questions = edit_quiz_data.get('num_questions')
    # redirect if current user is not owner of quiz
    user_is_owner = (
        edit_quiz_data.get('quiz_owner_id') == 
            ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )

    if not user_is_owner:
        flash('Cannot edit quiz - user is not quiz owner.', "invalid-action")
        return redirect(url_for(
            'view_quiz', 
            view_quiz_id=edit_quiz_id,
            _external=True, 
            _scheme='https'
        ))

    return render_template(
        "pages/edit-quiz.html",
        active_page="Edit Quiz",
        all_categories=all_categories,
        all_age_ranges=all_age_ranges,
        edit_quiz_data=edit_quiz_data,
        num_questions=num_questions,
        edit_quiz_id=edit_quiz_id,
        loggedIn=loggedIn
    )


# DELETE QUIZ #

@app.route("/delete-quiz/<delete_quiz_id>")
def delete_quiz(delete_quiz_id):
    """
    Read request.args to determine if request made during
    quiz creation or from edit_quiz page and construct
    appropriate url for redirects, read document from 
    quizzes collection by delete_quiz_id 
    (if not found redirect to previous url), check user 
    id value in session dict matches user_owner_id field 
    value in document (if not redirect to previous url), 
    use ids in quiz document questions array to count 
    questions in quiz then attempt to delete all questions 
    from questions collection, finally, check using 
    request.args for 'create_quiz_process' arg and 
    return redirect to create_quiz if equal to 'true' or
    redirect to discover if not. 

    Parameters:
    delete_quiz_id -- id for quiz document in mongodb to be deleted
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quiz.", "invalid-action")
        return redirect(url_for("login", _external=True, _scheme='https'))

    # use request.args to determine redirect location
    if request.args.get('create_quiz_process') == 'true':
        redirect_url = url_for('create_quiz', _external=True, _scheme='https')
    else:
        redirect_url = url_for('discover', _external=True, _scheme='https')

    # read document from quizzes collection by delete_quiz_id
    delete_quiz_data = mongo.db.quizzes.find_one(
        { 
            "_id": ObjectIdHelper.toObjectId(delete_quiz_id)
        },
        {
            "title": True,
            "quiz_owner_id": True,
            "questions": True
        }
    )
    if not delete_quiz_data:
        flash("Quiz not deleted - quiz not found.", "error")
        return redirect(redirect_url)
        
    # confirm current user is quiz owner
    user_is_owner = (
        delete_quiz_data.get('quiz_owner_id') == 
            ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )
    if not user_is_owner:
        flash("Quiz not deleted - you are not the owner.", "not-auth")
        return redirect(redirect_url)

    # find and delete quiz document by delete_quiz_id
    delete_quiz_result = mongo.db.quizzes.delete_one(
        { 
            "_id": ObjectIdHelper.toObjectId(delete_quiz_id)
        }
    )
    if not delete_quiz_result:
        flash(f"Quiz could not be deleted - try again later", "error")
        return redirect(redirect_url)

    # if quiz deleted successfully...
    # delete all associated from questions collection using quiz_data.questions ids
    num_questions = len(delete_quiz_data.get('questions'))
    if num_questions > 0: 
        delete_questions_result = mongo.db.questions.delete_many(
            { 
                "_id": { "$in": delete_quiz_data.get('questions') } 
            }
        )
        if (not delete_questions_result) or (not delete_questions_result.deleted_count == num_questions):
            flash(
                f"{delete_quiz_data.get('title')} was deleted but not all questions could be deleted.",
                "error" 
            )
        else:
            flash(f"Quiz and all questions were deleted.", "success")   

    else:
        flash(f"Quiz was deleted.", "success") 

    return redirect(redirect_url)


### CREATE, UPDATE, DELETE QUESTIONS ###

# CREATE QUESTION #

@app.route("/add-question/<quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):
    """
    Read quiz document from mongodb quizzes collection
    by quiz_id (if not found 
    redirect to create_quiz), read from request.args 
    to determine whether question is being added during
    a quiz creation process.
    
    If GET request: return render_template for 
    add-question template passing quiz data and 
    create_quiz_process boolean as arguments.

    If POST request: read data from request.form and
    try to insert new question document into mongodb 
    questions collection and store id of new document, 
    (if successful) try to update questions array of 
    quiz document identfied by quiz_id by pushing id 
    for new question, return redirect to add_question
    route (this route) passing create_quiz_process 
    boolean and quiz_id as arguments.

    Parameters:
    quiz_id -- id for quiz document in mongodb to which 
    created question id will be added 
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to add question.", "invalid-action")
        return redirect(url_for("login", _external=True, _scheme='https'))

    # read quiz data from db with quiz_id
    quiz_data = mongo.db.quizzes.find_one(
        { 
            "_id": ObjectIdHelper.toObjectId(quiz_id)
        },
        {
            "_id": False,
            "title": True,
            "num_questions": { "$size": "$questions" }
        }
    )
    if not quiz_data:
        flash("Quiz does not exist. First, create a new quiz.", "invalid-action")
        return redirect(url_for('create_quiz', _external=True, _scheme='https'))
    
    # if quiz identified by new_quiz_id exists...
    quiz_title = quiz_data.get('title')
    num_questions = quiz_data.get('num_questions')
    # determine if this endpoint was requested during a create quiz process
    create_quiz_process = request.args.get('create_quiz_process')

    # POST #
    if request.method == "POST":
        # read from request.form, construct form of questions document and 
        # insert to questions collection
        insert_result = mongo.db.questions.insert_one(
            {
                "question_text": request.form.get('new_question_text'),
                "correct_answer_index": int(request.form.get('correct_answer_index')),  # convert to int index for answers list
                "answers": [
                    {"answer_text": request.form.get('answer_0')},
                    {"answer_text": request.form.get('answer_1')},
                    {"answer_text": request.form.get('answer_2')},
                    {"answer_text": request.form.get('answer_3')}
                ]
            }
        )
        if not insert_result:
            flash('Question was not created.', "error")
        else:  
            # if insertion to questions collection successful...
            # update questions field of quiz document in quizzes collection identified by new_quiz_id 
            update_quiz_result = mongo.db.quizzes.update_one(
                { "_id": ObjectIdHelper.toObjectId(quiz_id) },
                { "$push": { "questions": ObjectIdHelper.toObjectId(insert_result.inserted_id) } }
            )
            if update_quiz_result:
                flash(f"Question {num_questions+1} was added to {quiz_title}.", "success")
            else:
                flash("Question was not added to quiz. Try again later.", "error")

        # send GET request to this endpoint
        return redirect(url_for(
            'add_question', 
            quiz_id=quiz_id,
            create_quiz_process=create_quiz_process,
            _external=True, 
            _scheme='https'
        ))

    # GET #
    return render_template(
        "pages/add-question.html",
        active_page="Add Question",
        loggedIn=loggedIn,
        quiz_id=quiz_id,
        quiz_title=quiz_title,
        num_questions=num_questions,
        create_quiz_process=create_quiz_process
    )


# UPDATE QUESTION #

@app.route(
    "/edit-question/<quiz_id>/<edit_question_id>", 
    methods=["GET", "POST"]
)
def edit_question(quiz_id, edit_question_id):
    """
    Read quiz document from mongo db quizzes collection
    by quiz_id including field for number of question
    identified by edit_question_id (if quiz not found, 
    return redirect to discover), check user 
    id value in session dict matches user_owner_id field 
    value in document (if not redirect to view_quiz), get
    value of edit_question_num field and check 
    edit_question_id was found in quiz_id questions array
    (if not redirect to view_quiz)

    If GET request: read question data from mongodb
    questions collection, return render_template for 
    edit-question template passing quiz_title, 
    edit_question_num and question data as arguments.

    If POST request: read request.form data and try
    to update question in mongodb questions 
    collection identified by edit_question_id, return 
    redirect to edit_quiz

    Parameters:
    quiz_id -- id for quiz document in mongodb quizzes
    collection to which question identified by 
    edit_question_id belongs.
    edit_question_id -- id for question document in 
    mongodb questions collection to be updated.
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to edit question", "invalid-action")
        return redirect(url_for("login", _external=True, _scheme='https'))

    # read quiz data from db with quiz_id
    quiz_data = mongo.db.quizzes.find_one(
        { 
            "_id": ObjectIdHelper.toObjectId(quiz_id)
        },
        {
            "title": True,
            "quiz_owner_id": True,
            "num_questions": { "$size": "$questions" },
            "edit_question_num": { 
                "$indexOfArray": 
                [
                    "$questions", 
                    ObjectIdHelper.toObjectId(edit_question_id)
                ] 
            }
        }
    )
    if not quiz_data:
        flash("Quiz not found.", "error")
        # redirect to where quiz id is not required
        return redirect(url_for('discover', _external=True, _scheme='https'))

    # confirm current user is quiz owner
    user_is_owner = (
        quiz_data.get('quiz_owner_id') ==
            ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )
    if not user_is_owner:
        flash("Cannot edit: current user is not the quiz owner", "invalid-action")
        return redirect(url_for(
            'view_quiz', 
            view_quiz_id=quiz_id,
            _external=True, 
            _scheme='https'
        ))

    # if quiz exists and current user is owner...    
    edit_question_index = quiz_data.get('edit_question_num', -1)  
    if edit_question_index == -1:
        flash("Cannot edit question - question not in quiz", "error")
        return redirect(url_for(
            'edit_quiz', 
            edit_quiz_id=quiz_id,
            _external=True, 
            _scheme='https'
        ))

    # POST #
    if request.method == "POST":
        # construct form of questions document for update
        update_question_result = mongo.db.questions.update_one(
            { "_id": ObjectIdHelper.toObjectId(edit_question_id) },
            {
                "$set": {
                    "question_text": request.form.get('edit_question_text'),
                    "correct_answer_index": int(request.form.get('correct_answer_index')),
                    "answers": [
                        {"answer_text": request.form.get('answer_0')},
                        {"answer_text": request.form.get('answer_1')},
                        {"answer_text": request.form.get('answer_2')},
                        {"answer_text": request.form.get('answer_3')}
                    ]
                }
            }
        ) 
        if update_question_result:
            flash("Question was updated.", "success")
        else:    
            flash("Question could not be updated. Try again later.", "error")

        return redirect(url_for(
            'edit_quiz', 
            edit_quiz_id=quiz_id,
            _external=True, 
            _scheme='https'
        ))

    # GET #
    # add 1 b/c $indexOfArray returns zero-based index
    edit_question_num = edit_question_index + 1
    quiz_title = quiz_data.get('title')
    # read question data from db with edit_question_id
    edit_question_data = mongo.db.questions.find_one(
        { 
            "_id": ObjectIdHelper.toObjectId(edit_question_id)
        }
    )

    return render_template(
        "pages/edit-question.html",
        active_page="Edit Question",
        loggedIn=loggedIn,
        quiz_id=quiz_id,
        edit_question_id=edit_question_id,
        edit_question_data=edit_question_data,
        quiz_title=quiz_title,
        edit_question_num=edit_question_num
    )


# DELETE QUESTION #

@app.route("/delete-question/<quiz_id>/<delete_question_id>")
def delete_question(quiz_id, delete_question_id):
    """
    Read quiz data from mongodb quizzes collection by quiz_id
    (if not found redirect to discover), check user 
    id value in session dict matches user_owner_id field 
    value in document (if not return redirect to view_quiz), 
    try to update questions array of quiz document identified 
    by quiz_id by removing element matching delete_question_id
    (if not return redirect to edit_quiz), try to delete 
    question document identified by delete_question_id from 
    mongodb questions collection, return redirect to edit_quiz
    

    Parameters:
    quiz_id -- id for quiz document in mongodb quizzes collection
    that references question document to be deleted
    delete_question_id -- id for question document in mongo db
    questions collection to be deleted
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to delete a quiz.", "invalid-action")
        return redirect(url_for("login", _external=True, _scheme='https'))

    # read document from quizzes collection by quiz_id
    quiz_data = mongo.db.quizzes.find_one(
        { 
            "_id": ObjectIdHelper.toObjectId(quiz_id)
        },
        {
            "title": True,
            "quiz_owner_id": True,
            "questions": True
        }
    )
    if not quiz_data:
        flash("Quiz not found", "error")
        return redirect(url_for('discover', _external=True, _scheme='https'))
        
    # confirm current user is quiz owner
    user_is_owner = (
        quiz_data.get('quiz_owner_id') == 
            ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )
    if not user_is_owner:
        flash("Question not deleted - user is not the quiz owner.", "invalid-action")
        return redirect(url_for(
            'view_quiz', 
            view_quiz_id=quiz_id,
            _external=True, 
            _scheme='https'
        ))

    # try to remove delete_quiz_id from quiz_id questions array
    update_quiz_questions_result = mongo.db.quizzes.update_one(
        { "_id": ObjectIdHelper.toObjectId(quiz_id) },
        { "$pull": { "questions": ObjectIdHelper.toObjectId(delete_question_id) } }
    )
    if not update_quiz_questions_result:
        flash("Question could not be deleted from quiz - try again later.", "error")
        return redirect(url_for(
            'edit_quiz', 
            edit_quiz_id=quiz_id,
            _external=True, 
            _scheme='https'
        ))

    # if quiz_id questions array is updated successfully, try to delete question
    mongo.db.questions.delete_one(
        { 
            "_id": ObjectIdHelper.toObjectId(delete_question_id)
        }
    )
    flash(f"Question was deleted from {quiz_data.get('title')}", "success")
    
    return redirect(url_for(
        'edit_quiz', 
        edit_quiz_id=quiz_id,
        _external=True,
        _scheme='https'
    ))


### START APP ###

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG") == "True"
    )

