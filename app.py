from flask import Flask, render_template, redirect, flash, url_for
from dotenv import load_dotenv
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from models import User, Post
import os
load_dotenv()

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

posts = [
    {
        'title': 'First Post',
        'content': 'This is my first post',
        'author': 'Kausik',
        'date': '28/11/24'
    }
]


@app.route('/')
@app.route('/home', endpoint='home')
def main():
    return render_template('index.html', title=None, posts=posts)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)
