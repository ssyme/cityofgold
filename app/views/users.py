from os import getcwd
from os.path import join, splitext
from random import SystemRandom
from subprocess import check_output

from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse

from ..forms import LoginForm, RegisterForm, EditProfileForm
from ..models import User, Board, Post
from ..extensions import db
from ..settings import UPLOAD_FOLDER

users = Blueprint("users", __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("No such user or incorrect password")
            return redirect(url_for('users.login'))
        login_user(user)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("main.index")
        return redirect(next_page)

    boards = list(sorted(Board.query.all(),
                         key=lambda x: x.hits, reverse=True))[:5]
    sizeofmedia = check_output(["du", "-h", "app/static/media/users"]).decode(
        ).split("\t")[0]
    sizeoftext = check_output(["du", "-h", "app/neochina.sqlite3"]).decode(
        ).split("\t")[0]
    return render_template("login.html", form=form, boards=boards,
                           sizeofmedia=sizeofmedia,
                           sizeoftext=sizeoftext,
                           nousers=len(Board.query.all()),
                           noposts=len(Post.query.all()))

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.login"))

    boards = list(sorted(Board.query.all(),
                         key=lambda x: x.hits, reverse=True))[:5]
    sizeofmedia = check_output(["du", "-h", "app/static/media/users"]).decode(
        ).split("\t")[0]
    sizeoftext = check_output(["du", "-h", "app/neochina.sqlite3"]).decode(
        ).split("\t")[0]
    return render_template("register.html", form=form, boards=boards,
                           sizeofmedia=sizeofmedia.lower(),
                           sizeoftext=sizeoftext.lower(),
                           nousers=len(Board.query.all()),
                           noposts=len(Post.query.all()))

@users.route("/<username>", methods=["GET", "POST"])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return abort(404, f"No such user '{username}' exists!")
    
    form = EditProfileForm()
    if form.validate_on_submit() and user == current_user:
        if form.bio.data:
            user.bio = form.bio.data
            db.session.commit()
            
        if form.avatar.data:
            randomness = SystemRandom().randint(9999,99999)
            filename = secure_filename(
                user.username + str(randomness) + \
                splitext(form.avatar.data.filename)[1])
            request.files[form.avatar.name].save(join(
                getcwd(), "app", UPLOAD_FOLDER, "users",
                filename))
            user.avatar = filename
            db.session.commit()
            
        return redirect(url_for("users.profile",
                                username=user.username))

    boards = list(sorted(Board.query.all(),
                         key=lambda x: x.hits, reverse=True))[:5]
    sizeofmedia = check_output(["du", "-h", "app/static/media/users"]).decode(
        ).split("\t")[0]
    sizeoftext = check_output(["du", "-h", "app/neochina.sqlite3"]).decode(
        ).split("\t")[0]
    return render_template("profile.html", user=user, form=form, boards=boards,
                           sizeofmedia=sizeofmedia.lower(),
                           sizeoftext=sizeoftext.lower(),
                           nousers=len(Board.query.all()),
                           noposts=len(Post.query.all()))
