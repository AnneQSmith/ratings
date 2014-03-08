from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    print user_list
    return render_template("user_list.html", users=user_list)

# Display a single user record
@app.route("/user/<id>", methods=['GET'])
def view_user(id):
    # Display the user record and update form
    pass

# Create a new user
@app.route("/user/new", methods=['GET'])
def new_user_form():
    # Display an HTML form to create a new user
    pass

@app.route("/user/new", methods=['POST'])
def new_user():
    # Get data for user from request.form

    # Create the user object

    # commit to database
    pass

# Update an existing user
@app.route("/user/<id>", methods=['POST'])
def update_user(id):
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