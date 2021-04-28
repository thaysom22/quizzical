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

    return render_template("pages/landing.html", 
        loggedIn=loggedIn,
        active_page="Welcome")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if loggedIn:
        return redirect(url_for("profile"))
    
    if request.method == "GET":
        return render_template("pages/login.html", 
            loggedIn=loggedIn,
            active_page="Log in")

    username_form = request.form.get("username").lower()  # get username from form (case-sensitive)
    existing_user = mongo.db.users.find_one(
        {
            "username": username_form
        }
    ) 
    
    if not existing_user:
        flash("Incorrect Username and/or Password")  # notify user of failure
        return redirect(url_for("login"))

    password_form = request.form.get("password")  # get password from form (not case-sensitive)
    correct_password = check_password_hash(
        existing_user["password"], password_form)

    if not correct_password:
        flash("Incorrect Username and/or Password")  # notify user of failure
        return redirect(url_for("login")) 

    # use existing_user dict to get category and age_range data from respective collections
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
            active_page="Register", 
            all_categories=all_categories,
            all_age_ranges=all_age_ranges)

    # if request.method == "POST":
    username_form = request.form.get("username").lower()  # form input validation done client-side
    existing_user = mongo.db.users.find_one(
        {
            "username": username_form
        }
    )
    
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
        "user_category_id": ObjectIdHelper.toObjectId(category_form_id),  
        "user_age_range_id": ObjectIdHelper.toObjectId(age_range_form_id)  
    }

    insert_new_user_result = mongo.db.users.insert_one(new_user_db)
    if not insert_new_user_result:
        flash("Could not register account, please try again later.")
        return redirect(url_for("register"))
    
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
    
    flash(f"Welcome to Quizzical, {username_form}") 
    
    return redirect(url_for("discover"))


@app.route("/discover")
def discover():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        return redirect(url_for("landing"))
    
    # read all categories and all age_ranges from db
    all_categories = list(mongo.db.categories
        .find(sort=[("category_name", 1)]))
    all_age_ranges = list(mongo.db.age_ranges
        .find(sort=[("order", 1)]))
    
    # read from quizzes collection by 
    # credit for "$arrayElemAt" workaround to use $loopup as findOne: https://stackoverflow.com/questions/37691727/how-to-use-mongodbs-aggregate-lookup-as-findone  
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

    # query quizzes collection by age_range
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
        

@app.route("/search", methods=["GET", "POST"])
def search():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to search quizzes")
        return redirect(url_for("login"))
       
    username = session.get("user").get("username") 
    # use request.args to parse optional url params. CREDIT: https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask 
    request_args = request.args
    if request.method == "GET":
        all_quizzes = request_args.get('all_quizzes')
        recc = request_args.get('recc')
        category = request_args.get('category')
        age_range = request_args.get('age_range')
        search_query = None 
        if all_quizzes == "true":
            search_results = list(mongo.db.quizzes.aggregate([
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
            return redirect(url_for("discover"))  # GET request to /search endpoint w/o required url parameters

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

    return render_template("pages/search.html",
        active_page="Search", 
        username=username,
        loggedIn=loggedIn,
        search_query=search_query,
        search_results=search_results
    )


### CREATE, READ, UPDATE, DELETE QUIZZES ###

# CREATE QUIZ #

@app.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes")
        return redirect(url_for("login"))

    if request.method == "GET":
        all_categories = list(mongo.db.categories
            .find(sort=[("category_name", 1)]))
        all_age_ranges = list(mongo.db.age_ranges
            .find(sort=[("order", 1)]))
        
        return render_template(
            "pages/create-quiz.html",
            active_page="Create Quiz", 
            loggedIn=loggedIn,
            all_categories=all_categories,
            all_age_ranges=all_age_ranges
        )
    
    # if request.method == "POST":
    new_quiz_data = {
        "title": request.form.get('create_quiz_title'),
        "quiz_owner_id": ObjectIdHelper.toObjectId(session.get("user").get("_id")),
        "quiz_category_id": ObjectIdHelper.toObjectId(request.form.get('create_quiz_category')),  
        "quiz_age_range_id": ObjectIdHelper.toObjectId(request.form.get('create_quiz_age_range')),
        "questions": []  
    }
    
    insert_result = mongo.db.quizzes.insert_one(new_quiz_data)
    if insert_result:
        new_quiz_id = insert_result.inserted_id
        flash(f"{request.form.get('create_quiz_title')} has been created")
        
        return redirect(url_for(
            'add_question', 
            quiz_id=new_quiz_id,
        ))

    else:
        flash('Error. Quiz was not created. Try again later.')    
        
        return redirect(url_for("create_quiz"))


# READ QUIZ #

@app.route("/view_quiz/<view_quiz_id>")
def view_quiz(view_quiz_id):
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes")
        return redirect(url_for("login"))

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
        return redirect(url_for('discover'))
    
    # view_quiz_data is a one-element list so access first element
    view_quiz_data = view_quiz_data[0]
    # view-quiz.html template needs to know if current user is owner of viewed quiz
    user_is_owner = (
        view_quiz_data.get('quiz_owner_id') == ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )
    num_questions = view_quiz_data.get('num_questions')

    return render_template("pages/view-quiz.html",
            active_page="View Quiz",
            view_quiz_id=view_quiz_id, 
            user_is_owner=user_is_owner,
            view_quiz_data=view_quiz_data,
            num_questions=num_questions,
            loggedIn=loggedIn)


# UPDATE QUIZ #

@app.route("/edit_quiz/<edit_quiz_id>", methods=["GET", "POST"])
def edit_quiz(edit_quiz_id):
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to view your profile")
        return redirect(url_for("login"))

    if request.method == "POST":
        # input values have been validated client-side
        new_title = request.form.get('edit-title')
        new_category = request.form.get('edit-category')
        new_age_range = request.form.get('edit-age-range')
        # update quiz document in db
        update_quiz_result = mongo.db.quizzes.update_one(
            { "_id": ObjectIdHelper.toObjectId(edit_quiz_id) },
            { 
                "$set": { 
                    "title": new_title,
                    "quiz_category_id": ObjectIdHelper.toObjectId(new_category),
                    "quiz_age_range_id": ObjectIdHelper.toObjectId(new_age_range),
                } 
            }
        )    
        # update successful guard clause
        if not update_quiz_result:
            flash("Error: quiz could not be updated. Try again later.")
        else:
            flash("Quiz updated.")

        # redirect to view same quiz
        return redirect(url_for('view_quiz', view_quiz_id=edit_quiz_id))

    
    # if request.method == "GET":
    # read all categories and all age_ranges from db
    all_categories = list(mongo.db.categories
        .find(sort=[("category_name", 1)]))
    all_age_ranges = list(mongo.db.age_ranges
        .find(sort=[("order", 1)]))

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
        flash('Error: quiz not found')
        return redirect(url_for('discover'))

    # check user is owner by reading from db with edit_quiz_id
    # edit_quiz_data is a one-element list so access first element
    edit_quiz_data = edit_quiz_data[0]
    # redirect if current user is not owner of quiz
    user_is_owner = (
        edit_quiz_data.get('quiz_owner_id') == ObjectIdHelper.toObjectId(session.get('user').get('_id'))
    )

    if not user_is_owner:
        flash('Warning: cannot edit quiz - current user is not quiz owner')
        return redirect(url_for('view_quiz', view_quiz_id=edit_quiz_id))

    num_questions = edit_quiz_data.get('num_questions')

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

@app.route("/delete_quiz/<delete_quiz_id>")
def delete_quiz(delete_quiz_id):
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes")
        return redirect(url_for("login"))

    # return and delete quiz document by delete_quiz_id
    delete_quiz_data = mongo.db.quizzes.find_one_and_delete(
        { 
            "_id": ObjectIdHelper.toObjectId(delete_quiz_id)
        }
    )

    if not delete_quiz_data:
        flash(f"Error: {delete_quiz_data.get('title')} quiz could not be deleted. Try again later")
        return redirect(url_for('add_question', quiz_id=delete_quiz_id))


    # if quiz deleted successfully...
    # delete all associated from questions collection using quiz data.questions ids 
    delete_result = mongo.db.questions.delete_many(
        { 
            "_id": { "$in": delete_quiz_data.get('questions') } 
        }
    )

    if (not delete_result) or (not delete_result.deleted_count == len(delete_quiz_data.get('questions'))):
        flash(f"Error: {delete_quiz_data.get('title')} was deleted but not all questions could be deleted")
    else:
        flash(f"{delete_quiz_data.get('title')} quiz and all questions were deleted")
    
    return redirect(url_for('create_quiz'))


### CREATE, UPDATE, DELETE QUESTIONS ###

# CREATE QUESTION #

@app.route("/add_question/<quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes")
        return redirect(url_for("login"))

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
        flash("Error: Quiz does not exist. Create a new quiz...")
        return redirect(url_for('create_quiz'))
    
    # if quiz identified by new_quiz_id exists...
    quiz_title = quiz_data.get('title')
    num_questions = quiz_data.get('num_questions')

    if request.method == "POST":
        # construct form of questions document and insert to questions collection
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
            flash('Error: question was not created. Try again later.')
            # GET request to this endpoint
            return redirect(url_for(
                'add_question', 
                quiz_id=quiz_id,
            ))

        # if insertion to questions collection successful...
        # update questions field of quiz document in quizzes collection identified by new_quiz_id 
        update_quiz_result = mongo.db.quizzes.update_one(
            { "_id": ObjectIdHelper.toObjectId(quiz_id) },
            { "$push": { "questions": ObjectIdHelper.toObjectId(insert_result.inserted_id) } }
        )
        
        if update_quiz_result:
            flash(f"Question {num_questions+1} was added to {quiz_title}.")
        else:
            flash("Error: question was not added to quiz. Try again later.")

        # GET request to this endpoint
        return redirect(url_for(
            'add_question', 
            quiz_id=quiz_id,
        ))

    # GET request
    return render_template(
        "pages/add-question.html",
        active_page="Add Question",
        loggedIn=loggedIn,
        quiz_id=quiz_id,
        quiz_title=quiz_title,
        num_questions=num_questions,
    )


# UPDATE QUESTION #

@app.route("/edit_question/<quiz_id>/<edit_question_id>", methods=["GET", "POST"])
def edit_question(quiz_id, edit_question_id):
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes")
        return redirect(url_for("login"))


    # GET request

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
        flash("Error: Quiz not found. Cannot edit question. Try again later.")
        # redirect to where quiz id not required
        return redirect(url_for('discover'))
    
    # if quiz identified by new_quiz_id exists...
    quiz_title = quiz_data.get('title')
    num_questions = quiz_data.get('num_questions')

    # read question data from db
    


    return render_template(
        "pages/edit-question.html",
        active_page="Edit Question",
        loggedIn=loggedIn,
        edit_quiz_id=edit_quiz_id,
        edit_question_id=edit_question_id,
        quiz_title=quiz_title,
        num_questions=num_questions
    )


# DELETE QUESTION #

@app.route("/delete_question/<quiz_id>/<delete_question_id>")
def delete_question(quiz_id, delete_question_id):
    """
    docstring here
    """
    loggedIn = 'user' in session
    if not loggedIn:
        flash("Login first to create quizzes")
        return redirect(url_for("login"))

    
    return redirect(url_for('edit_quiz', edit_quiz_id=quiz_id))


        






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
        active_page=f"Profile: {username}",
        username=username,
        loggedIn=loggedIn)


### START APP ###
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG") == "True"
    )

