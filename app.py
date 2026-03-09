from flask import Flask, flash, redirect, render_template, request, url_for
import os
from models import db
from data_manager import DataManager

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
def user_movies(user_id):
    favorite_movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=favorite_movies)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    pass


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def functionb():
    pass


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def functionc():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
