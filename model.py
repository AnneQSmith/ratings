from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey, update
from sqlalchemy.orm import relationship, backref
import correlation
import os

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE,
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        if not self.ratings: 
            return None
        
        print ("We got past ther first line in predict_rating")
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
            for r in other_ratings ]
        similarities.sort(reverse = True)
        top = similarities[0]

        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        prediction = sum([ sim * r.rating for sim, r in similarities ])
        denominator = sum( sim[0] for sim in similarities )
        prediction = float(prediction)/denominator
        return prediction

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    released_at = Column(Date(timezone=False), nullable=True)
    imdb_url = Column(String(156), nullable=True)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Integer)
    user = relationship("User",
            backref=backref("ratings", order_by=id))
    movie = relationship("Movie",
            backref=backref("ratings", order_by=id))


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()

