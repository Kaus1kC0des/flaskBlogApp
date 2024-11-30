from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from email_validator import validate_email
from flaskBlog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(3, 20)]
    )

    email = EmailField(
        'Email',
        validators=[Email(), DataRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(5, 25)]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), Length(5, 25), EqualTo('password')]
    )

    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose another username.')

    @staticmethod
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("An User with that email exists. Please provide a different email!")


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[Email(), DataRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(5, 25)]
    )

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
