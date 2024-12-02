from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flaskBlog.models import User
from flask_login import current_user


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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose another username.')

    def validate_email(self,email):
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


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=29)]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    picture = FileField(label='Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already taken! Please choose an another username.")

    def validate_email(self, email):
        if email != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("An User with that email exists. Please provide a different email!")