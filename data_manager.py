from models import db, User, Movie
from sqlalchemy.exc import SQLAlchemyError


class DataManager:
    def create_user(self, user_name):
        """Creates a new user and saves it in database
        params: name of new user"""
        new_user = User(name=user_name)
        db.session.add(new_user)
        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def get_all_users(self):
        """Fetches list of all users from database"""
        user_list = db.session.query(User).all()
        return user_list

    def get_user_by_name(self, user_name):
        """Checks if the user name already exists"""
        is_existing = User.query.filter(User.name == user_name).first()
        if is_existing:
            return True
        return False

    def get_movies(self, user_id):
        """Gets all movies filtered by user from database
        prams: user_id"""
        user_movies = (
            db.session.query(Movie).filter(Movie.user_id == user_id).all()
        )  # Lange Schreibweise
        # user = User.query.get(user_id)
        # neuere Alternative: user = db.session.get(User, user_id)
        # ermittle User, speichere id des users (z.B. 5)
        # user_movies = (user.movies)  # die movies vom user (übersetzt sowas wie user5.movies)
        return user_movies

    def is_movie_already_existing(self, user_id, title):
        """Checks whether the movie already exists in a users collection.
        params: user_id, title of the movie"""
        is_existing = Movie.query.filter(
            Movie.title == title, Movie.user_id == user_id
        ).first()
        if is_existing:
            return True
        return False

    def add_movie(self, movie):
        """Adds a movie to database.
        params: movie"""
        db.session.add(movie)
        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def update_movie(self, movie_id, new_rating):
        """Updates the rating of a movie in the database.
        params: movie-id, new_rating"""
        movie_to_update = Movie.query.get(movie_id)
        if movie_to_update:
            movie_to_update.rating = new_rating
            try:
                db.session.commit()
                return True
            except SQLAlchemyError:
                db.session.rollback()
                return False

    def delete_movie(self, movie_id):
        """Deletes a movie in the database.
        params: movie_id"""
        movie_to_delete = Movie.query.get(movie_id)
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            try:
                db.session.commit()
                return True
            except SQLAlchemyError:
                db.session.rollback()
                return False
