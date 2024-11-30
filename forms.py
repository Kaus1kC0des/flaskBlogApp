from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo
import email_validator


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
