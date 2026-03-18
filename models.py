from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"User {self.id}: {self.name}"

    def __str__(self):
        return f"User: {self.name}"


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(255))
    year = db.Column(db.Integer)
    img = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="movies")

    def __repr__(self):
        return f"Movie {self.id}: {self.title}"

    def __str__(self):
        return f"Movie: {self.title}: {self.year}, {self.rating}"
