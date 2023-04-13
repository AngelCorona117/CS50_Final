from flask_wtf import FlaskForm
from wtforms import validators

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)

from wtforms import StringField, PasswordField, SubmitField, BooleanField


class SignupForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[
            DataRequired(),
            validators.Length(min=3, max=20),
            validators.Regexp(
                "^[A-Za-z0-9_]{0,20}$",
                message="Username must have only letters, numbers, and underscores",
            ),
        ],
    )
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            validators.Length(min=3, max=20),
            validators.Regexp(
                "^[A-Za-z0-9_]{0,20}$",
                message="Username must have only letters, numbers, and underscores",
            ),
        ],
    )
    confirmation = PasswordField(
        label="Confirmation",
        validators=[
            DataRequired(),
            validators.Length(min=3, max=20),
            validators.Regexp(
                "^[A-Za-z0-9_]{0,20}$",
                message="Username must have only letters, numbers, and underscores",
            ),
        ],
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")
