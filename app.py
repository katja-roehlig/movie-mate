from flask import Flask, flash, redirect, render_template, request, url_for
import os
from models import db, Movie
from data_manager import DataManager
import api.api_handler as api

app = Flask(__name__)

app.secret_key = "my not so secret password"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.sqlite')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
data_manager = DataManager()

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    users = data_manager.get_all_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def add_user():
    new_user = request.form.get("user_name")
    if new_user:
        data_manager.create_user(new_user)
        flash("User successfully added!")
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def show_movies(user_id):
    favorite_movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=favorite_movies, current_user=user_id)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_new_movie(user_id):
    movie_title = request.form.get("title")
    if movie_title:
        title_existing = data_manager.is_movie_already_existing(user_id, movie_title)
        if title_existing:
            flash("Movie already exists!")
            return redirect(url_for("show_movies", user_id=user_id))
        new_movie = api.get_movie_info_per_title(movie_title)
        if not new_movie:
            flash("Movie was not found.")
            return redirect(url_for("show_movies", user_id=user_id))
        title, publication_year, image = new_movie
        movie = Movie(user_id=user_id, title=title, year=publication_year, img=image)
        data_manager.add_movie(movie)
    return redirect(url_for("show_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_rating(user_id, movie_id):
    rating = request.form.get("rating")
    rating = float(rating)
    print(type(rating))
    if not rating:
        return redirect(url_for("show_movies", user_id=user_id))
    if 1 <= rating <= 10:
        data_manager.update_movie(movie_id, rating)
        flash("Movie successfully updated")
        return redirect(url_for("show_movies", user_id=user_id))
    flash("Rating must be a number between 1 and 10.")
    return redirect(url_for("show_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    flash("Movie successfully deleted")
    return redirect(url_for("show_movies", user_id=user_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
