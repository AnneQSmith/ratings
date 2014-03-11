from flask import Flask, render_template, redirect, request, flash, session,url_for
import model

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route("/")
def index():
    return render_template("login_user.html")

    # user_list = model.session.query(model.User).limit(15).all()
    # return render_template("user_list.html", users=user_list)

@app.route("/user/login", methods=['GET'])
def user_login_form():
    return render_template("login_user.html")


@app.route("/logout", methods=['GET'])
def logout():
    # session['user_id'] = None
    # session['username'] = None
    session.clear()
    flash("Re-enter credentials to rate more movies")
    return render_template("login_user.html")

@app.route("/user/login", methods=['POST'])
def user_login():
     # Get login data for user from login-user form
    username = request.form.get("username")
    password = request.form.get("password")

    user_list = model.session.query(model.User).filter_by(email=username, password=password).all()
    if len(user_list) == 0:
        flash("User does not exist.")
        return render_template("login_user.html")
    elif (user_list[0].email == None) | (user_list[0].email == ""):
        flash("Enter an id")
        return render_template("login_user.html")
    else:
        #Note we are ignoring the case in which there are multiple users with the credentials
        flash("User authenticated.")
        session['username'] = username
        id = user_list[0].id
        session['user_id'] = id
        print session, session['username'], session['user_id']
        ratings = model.session.query(model.Rating).filter_by(user_id=id)    
    return render_template("view_user.html", user=user_list[0], ratings=ratings)    
    



@app.route("/search", methods=["GET"])
def display_search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    movies = model.session.query(model.Movie).\
            filter(model.Movie.name.ilike("%" + query + "%")).\
            limit(50).all()
    for movie in movies:
        print movie.name

    return render_template("results.html", movies=movies)

@app.route("/rate/<int:id>", methods=["POST"])
def rate_movie(id):
    rating_number = int(request.form['rating'])
    user_id = session['user_id']

    rating = model.session.query(model.Rating).filter_by(user_id=user_id, movie_id=id).first()

    if not rating:
        flash("Rating added", "success")
        rating = model.Rating(user_id=user_id, movie_id=id)
        model.session.add(rating)
    else:
        flash("Rating updated", "success")

    rating.rating = rating_number
    model.session.commit()

    user = model.session.query(model.User).get(user_id)
    ratings = model.session.query(model.Rating).filter_by(user_id=user_id)    
    return render_template("view_user.html", user=user, ratings=ratings)    


@app.route("/movie/<int:id>", methods=["GET"])
def view_movie(id):
    movie = model.session.query(model.Movie).get(id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    current_user_id = session['user_id']
    for r in ratings:
        if r.user_id == current_user_id:
            user_rating = r
        rating_nums.append(r.rating)
    n_ratings = len(rating_nums)
    if n_ratings > 0:
        avg_rating = float(sum(rating_nums))/n_ratings
    else:
        avg_rating = None

    prediction = None
    if not user_rating:
        user = model.session.query(model.User).get(current_user_id) 
        prediction = user.predict_rating(movie)
        print current_user_id, prediction, movie.name
    
    return render_template("movie.html", movie=movie, 
            average=avg_rating, user_rating=user_rating,
            prediction = prediction)


@app.route("/search/movie", methods=['POST'])
def movie_search():
    name = request.form.get("name")
    print name
    movies = model.session.query(model.Movie).filter_by(name=name).all()
    # for m in movies:
    #      print movies[m].name
    # return "blah blah blah"

@app.route("/list/movies", methods=['GET'])
def list_movies():
    movie_list = model.session.query(model.Movie).limit(2000).all()

    return render_template("movie_list.html", movies=movie_list)

# Display a single user record
@app.route("/user/<id>", methods=['GET'])
def view_user(id):
    # Display the user record and update form

    print "trying not to crash with id # ", id
    user = model.session.query(model.User).get(id)
    ratings = model.session.query(model.Rating).filter_by(user_id=id)
    return render_template("view_user.html", user=user, ratings=ratings)

# Create a new user
@app.route("/user/new", methods=['GET'])
def new_user_form():
    # Display an HTML form to create a new user
    return render_template("new_user_form.html")
    #return redirect(url_for("new_user"))

@app.route("/user/new", methods=['POST'])
def new_user():
    username = request.form.get("username")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

# check whether name exists:
    existinguserlist = model.session.query(model.User).filter_by(email=username).all()
    if len(existinguserlist) > 0:
        flash("That user name is taken, try again")
        return render_template("new_user_form.html")

# Go ahead and assume it's valid input no matter what the crazy user did    
    else:            
        user = model.User(email=username, password=password,age=age, zipcode=zipcode)
        model.session.add(user)
        model.session.commit()
        #Automatically create a session for this user
        session["user_id"] = user.id
        session["username"] = user.email

        print username, password,age,zipcode,user.id
        return redirect(url_for("view_user", id=user.id))
   # return render_template("view_user.html",user=user, user.id)


@app.route("/user/edit/<id>", methods=['GET'])
def edit_user_form(id):
    print "hello we made it to edit_user from get and user id = " ,id
    user = model.session.query(model.User).get(id)
    print "hello we made it to edit_user from get and user id = " ,user.id
    return render_template("edit_user.html",user=user,id=id)
  

@app.route("/user/edit/<id>", methods=['POST'])
def edit_user(id):
#still no type checking on input parameters
    user = model.session.query(model.User).get(id)
    username = user.email
    print " username = ",username

#TODO check session information    
# if session['username'] != username:
#     flash("you must login before you can edit")
#     return render_template("login_user.html")
# else:
    newusername = request.form.get("username")
    if newusername:
        user.email = newusername
        print newusername
    
    newpassword = request.form.get("password")
    if newpassword:
        user.password = newpassword
        print newpassword

    newage = request.form.get("age")
    if newage:
        user.age = newage
        print newage

    newzip = request.form.get("zipcode")
    if newzip:
        user.zipcode = newzip
        print newzip

    print "hopefully these made it to the db", user.email, user.password, user.age, user.zipcode, user.id

    model.session.commit() 
    
    ratings = model.session.query(model.Rating).filter_by(user_id=id)

    return render_template("view_user.html", user=user, ratings=ratings)  
    #return "blah"   
  




if __name__ == "__main__":
    app.run(debug = True)