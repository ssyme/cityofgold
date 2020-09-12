from flask import Blueprint, render_template

from ..models import Board, Post

from .boards import boards
from .users import users

main = Blueprint("main", __name__)

@main.route("/")
def index():
    boards = list(sorted(Board.query.all(),
                         key=lambda x: x.hits, reverse=True))[:5]
    topposts = list(sorted(Post.query.all(), key=lambda x: x.hits,
                           reverse=True))[:5]
    return render_template("index.html", boards=boards, topposts=topposts)

"""The following function shall immenently be extirpated and can thus
safely and charitably be ignored."""
@main.route("/createdb")
def createall():
    from ..extensions import db

    db.create_all()

    from ..models import User, Board
    
    u1 = User(username="cat99")
    u1.set_password("password123")
    u2 = User(username="salo")
    u2.set_password("table")

    b1 = Board(name="lounge")
    b2 = Board(name="news")
    b3 = Board(name="literature")
    b4 = Board(name="history")

    db.session.add(u1)
    db.session.add(u2)

    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)
    db.session.add(b4)    

    db.session.commit()
    return "success"
