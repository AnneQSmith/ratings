import model
import csv
import datetime
import re

#
#  before this will work, execute the following:
# python -i model.py
# In your interactive python shell that results, type in
# engine = create_engine("sqlite:///ratings.db", echo=True)
# Now, open a second terminal window and go to your project folder, do an 
#       ls to verify that ratings.db does not exist.
# In your first window, type the following, and something that appears to 
#           be a sql table schema will scroll by.
# Base.metadata.create_all(engine)
# Back in your second window, do another ls You should see a ratings.db file. Invoke sqlite on this 


def load_users(session):
    # use u.user
    with open('./seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, age, gender, occupation, zipcode = row
            id = int(id)          
            age = int(age)            
            user = model.User(id=id, email=None, password=None,  age=age, zipcode=zipcode)
            session.add(user)
        session.commit()
      
def load_movies(session):
    # use u.item
    with open('./seed_data/u.item', 'rb') as f:
        reader = csv.reader(f)   
        for row in reader:
            values = ','.join(row)
            values = values.split('|')
            item_id = int(values[0])
            title = values[1].decode("latin_1")
            title = re.sub("\(\d{4}\)", "",title)
            title = title.strip()
            if values[2] == '':
                date = None           
            else:
                date = datetime.datetime.strptime(values[2], "%d-%b-%Y").date()

            movie = model.Movie(id=item_id, name=title, released_at=date, imdb_url=values[4])
            session.add(movie)
        session.commit()    

def load_ratings(session):
    # use u.data
    with open('./seed_data/u.data', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            values = row[0].split( )
            rating = model.Rating(movie_id=int(values[1]), user_id=int(values[0]), rating=int(values[2]))
            session.add(rating)
        session.commit()          

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_ratings(session)
    load_movies(session)
    pass 

if __name__ == "__main__":
    s = model.session
    main(s)
