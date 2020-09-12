from os.path import splitext

from flask import config

from flask_wtf import FlaskForm
from wtforms.validators import Required, EqualTo, ValidationError

from wtforms import (
    PasswordField,
    FileField,
    SubmitField,
    TextAreaField,
    TextField
)

from .models import User
from .settings import ALLOWED_EXTENSIONS

class RegisterForm(FlaskForm):
    username = TextField("Username", [Required()])
    password = PasswordField("Password", [Required()])
    confirmpassword = PasswordField("Confirm Password", [
        Required(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                "It seems that username is taken, try another.")


class LoginForm(FlaskForm):
    username = TextField("Username", [Required()])
    password = PasswordField("Password", [Required()])
    submit = SubmitField("Login")

class NewPostForm(FlaskForm):
    content = TextAreaField("Text", [Required("Posts must contain content")])
    submit = SubmitField("Post")

class NewReplyForm(FlaskForm):
    content = TextAreaField("Text", [Required("Replies must have a body")])
    submit = SubmitField("Reply")

class EditProfileForm(FlaskForm):
    bio = TextAreaField("New Bio")
    avatar = FileField("New Avatar")
    submit = SubmitField("Save changes")

    def validate_avatar(self, avatar):
        if avatar.data:
            if splitext(avatar.data.filename)[1] not in ALLOWED_EXTENSIONS:
                print(splitext(avatar.data)[1])
                raise ValidationError("Please upload an image!")
