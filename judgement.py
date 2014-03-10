from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(150).all()
    return render_template("user_list.html", users=user_list)

# Display a single user record
@app.route("/user/<id>", methods=['GET'])
def view_user(id):
    # Display the user record and update form

    print "trying not to crash with id # ", id
    user = model.session.query(model.User).get(id)
    print user.age, user.zipcode
    return render_template("view_user.html", user=user)

# Create a new user
@app.route("/user/new", methods=['GET'])
def new_user_form():
    # Display an HTML form to create a new user
    return render_template("create_user.html")
    #return redirect(url_for("new_user"))

@app.route("/user/new", methods=['POST'])
def new_user():
    username = request.form.get("username")
    password = request.form.get("password")
    age = int(request.form.get("age"))
    zipcode = request.form.get("zipcode")

    user = model.User(email=username, password=password,age=age, zipcode=zipcode)
    model.session.add(user)
    model.session.commit()

    print username, password,age,zipcode
    return render_template("create_user.html")
    #return render_template("user_list.html", users=None)
    #return render_template("create_user.html")
    # Get data for user from request.form

    # Create the user object

    # commit to database
# Create a new user
@app.route("/user/edit/<id>", methods=['GET'])
def edit_user(id):
    # Display an HTML form to create a new user
    print "hello we made it to edit_user_form get"
    return render_template("edit_user.html")
  #  return render_template("edit_user.html", user)
    #return redirect(url_for("new_user"))

# @app.route("/user/edit/<id>", methods=['POST'])
# def edit_user(id):
#     # Display an HTML form to edit an new user
#     print "hello we made it to edit_user post"
#    #  username = request.form.get("username")
#    #  password = request.form.get("password")
#    #  age = int(request.form.get("age"))
#    #  zipcode = request.form.get("zipcode")

#    #  user = model.User(email=username, password=password,age=age, zipcode=zipcode)
#    #  #model.session.add(user)
#    # # model.session.commit()

#    #  print username, password,age,zipcode
#     return render_template("edit_user.html")
#    # return render_template("edit_user.html", user)
    #return redirect(url_for("new_user"))

# Update an existing user
# @app.route("/user/<id>", methods=['POST'])
# def update_user(id):
    # Query for the user from the database

    # Check that you actually got data from the database!?

    # Get data from request.form

    # Update the user object

    # Save (hint: commit) the user to the database 

    # redirect user to movie trailers on youtube for cute cat videos
    # (flash message to the user that their update worked)
    pass












    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)    

    

if __name__ == "__main__":
    app.run(debug = True)