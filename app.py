from flask import Flask, flash, redirect, render_template, request, url_for
import os
from models import db, Movie
from data_manager import DataManager
from dotenv import load_dotenv
import api.api_handler as api

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")
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
    """Handles the GET request to show the landing page.
    Shows all users on landing page"""
    users = data_manager.get_all_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def add_user():
    """Handles the POST request to add a new user."""
    new_user = request.form.get("user_name", "").strip()
    if not new_user:
        flash("Username cannot be empty.", "attention")
        return redirect(url_for("index"))
    if new_user:
        user_existing = data_manager.get_user_by_name(new_user)
        if user_existing:
            flash(f"Username '{new_user}' already exists.", "attention")
            return redirect(url_for("index"))
        if not data_manager.create_user(new_user):
            flash("Something went wrong. \nPlease try again", "error")
            return redirect(url_for("index"))
    flash("User successfully added!", "success")
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def show_movies(user_id):
    """Handles the GET request to show a list of movies filtered by the user"""
    favorite_movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=favorite_movies, current_user=user_id)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_new_movie(user_id):
    """
    Handles the POST request to add a new movie.
    Fetches details from OMDb API and saves them to the database.
    """
    movie_title = request.form.get("title", "").strip()
    if not movie_title:
        flash("You must enter a movie title!", "attention")
        return redirect(url_for("show_movies", user_id=user_id))

    title_existing = data_manager.is_movie_already_existing(user_id, movie_title)

    if title_existing:
        flash("Movie already exists!", "attention")
        return redirect(url_for("show_movies", user_id=user_id))

    new_movie = api.get_movie_info_per_title(movie_title)

    if new_movie is False:
        flash(
            "Movie was not found.\nPlease check the spelling of the title", "attention"
        )
        return redirect(url_for("show_movies", user_id=user_id))
    if new_movie is None:
        flash(
            "Unable to connect to the movie database. "
            "Please check your internet connection or try again later.",
            "error",
        )
        return redirect(url_for("show_movies", user_id=user_id))

    title, publication_year, director, image = new_movie

    movie = Movie(
        user_id=user_id,
        title=title,
        director=director,
        year=publication_year,
        img=image,
    )
    if not data_manager.add_movie(movie):
        flash("Something went wrong with the database. Please try again", "error")
        return redirect(url_for("show_movies", user_id=user_id))
    flash("Movie successfully added", "success")
    return redirect(url_for("show_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_rating(user_id, movie_id):
    """Handles the POST request to update the rating of a movie."""
    rating = request.form.get("rating")

    if not rating:
        return redirect(url_for("show_movies", user_id=user_id))
    try:
        rating = float(rating)
    except ValueError:
        flash("Please enter a number between 1 and 10", "attention")
        return redirect(url_for("show_movies", user_id=user_id))

    if not (1 <= rating <= 10):
        flash("Rating must be a number between 1 and 10.", "attention")
        return redirect(url_for("show_movies", user_id=user_id))

    if not data_manager.update_movie(movie_id, rating):
        flash("Something went wrong with the database. Please try again", "error")
        return redirect(url_for("show_movies", user_id=user_id))
    flash("Movie successfully updated", "success")
    return redirect(url_for("show_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete(user_id, movie_id):
    """Handles the POST request to delete a movie."""
    if not data_manager.delete_movie(movie_id):
        flash("Something went wrong with the database. Movie was not deleted.", "error")
        return redirect(url_for("show_movies", user_id=user_id))
    flash("Movie successfully deleted", "success")
    return redirect(url_for("show_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Handles the 404 error, if page is not found"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handles the 500 error"""
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
