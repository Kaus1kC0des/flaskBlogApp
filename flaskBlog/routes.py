from flask import render_template, redirect, flash, url_for
from flaskBlog import app
from flaskBlog.forms import LoginForm, RegistrationForm
from flaskBlog.models import User, Post

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


