from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import current_user

from ..forms import NewPostForm, NewReplyForm
from ..extensions import db
from ..models import Board, Post, Reply

boards = Blueprint("boards", __name__)

@boards.route("/<boardname>/", methods=["GET", "POST"])
def board(boardname):
    board = Board.query.filter_by(name=boardname).first()
    
    if request.method == "GET":
        board.hits+=1
        db.session.commit()
        
    form = NewPostForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return abort(403)
        p = Post(content=form.content.data, user=current_user,
                 board=board)
        board.posts.append(p)
        db.session.commit()
        return redirect(url_for("boards.board", boardname=board.name))

    boards = list(sorted(Board.query.all(),
                         key=lambda x: x.hits, reverse=True))[:5]
    return render_template("board.html", boards=boards, board=board, form=form,
                           posts=reversed(board.posts))

@boards.route("/<boardname>/post/<postid>", methods=["GET", "POST"])
def post(boardname, postid):
    board = Board.query.filter_by(name=boardname).first()
    post = Post.query.filter_by(id=postid).first()
    if not post or post.board != board:
        print('error retrieving post', post.board, board,
              post.board==board)
        return abort(404)
    
    if request.method == "GET":
        post.hits+=1
        db.session.commit()
        
    form = NewReplyForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return abort(403)
        r = Reply(content=form.content.data, user=current_user,
                  post=post)
        post.replies.append(r)
        db.session.commit()
        return redirect(url_for("boards.post", boardname=board.name,
                                postid=post.id))

    boards = list(sorted(Board.query.all(),
                         key=lambda x: x.hits, reverse=True))[:5]
    return render_template("post.html", boards=boards, post=post, form=form,
                           replies=post.replies)
