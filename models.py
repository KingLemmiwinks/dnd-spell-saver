"""SQLAlchemy models for DnD application."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)
    
    likes = db.relationship('Likes')

    # start_register
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate


class Likes(db.Model):
    """Mapping user likes to app."""

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)

    spell_index = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    spell_name = db.Column(db.String)


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
