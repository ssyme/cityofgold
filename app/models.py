from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime
from flask_login import UserMixin

from .extensions import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    joined = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Integer, default=0)
    bio = db.Column(db.String(300))
    avatar = db.Column(db.String(30))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Board(db.Model):
    __tablename__ = "boards"
    id = db.Column(db.Integer, primary_key=True)
    hits = db.Column(db.Integer, default=0)
    name = db.Column(db.String(10), nullable=False)
    locked = db.Column(db.Integer, default=0)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pinned = db.Column(db.Integer, default=0)
    hits = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("User", backref=
                           db.backref("posts", lazy=True))
    
    board_id = db.Column(db.Integer, db.ForeignKey("boards.id"),
                         nullable=False)
    board = db.relationship("Board", backref=
                            db.backref("posts", lazy=True))

class Reply(db.Model):
    __tablename__ = "replies"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("User", backref=
                           db.backref("replies", lazy=True))

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"),
                        nullable=False)
    post = db.relationship("Post", backref=
                           db.backref("replies", lazy=True))
