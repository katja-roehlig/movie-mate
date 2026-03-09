from models import db, User, Movie


class DataManager:
    def create_user(self, user_name):
        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()nein, das ist soweit klar! wo

    def get_all_users(self):
        user_list = db.session.query(User).all()
        return user_list

    def get_movies(self, user_id):
        # user_movies = db.session.query(Movie).filter(Movie.user_id == user_id).all() - Lange Schreibweise
        user = User.query.get(user_id)
        user_movies = user.movies
        return user_movies

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_rating):
        movie_to_update = Movie.query.get(movie_id)
        if movie_to_update:
            movie_to_update.rating = new_rating
            db.session.commit()

    def delete_movie(self, movie_id):
        movie_to_delete = Movie.query.get(movie_id)
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
