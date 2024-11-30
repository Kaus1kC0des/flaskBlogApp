from flask import render_template, redirect, flash, url_for, request
from flaskBlog import app, bcrypt, db
from flaskBlog.forms import LoginForm, RegistrationForm
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'title': 'First Post',
        'content': 'This is my first post',
        'author': 'Kausik',
        'date': '28/11/24'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title=None, posts=posts)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_pwd,
            )
            db.session.add(user)
            db.session.commit()
            flash(f"Account created successfully for {form.username.data}! You can now log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"An Error Occurred: {e}", 'danger')
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash(f"Login Unsuccessful! Please check your email and password", 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=["GET","POST"])
@login_required
def account():
    return render_template('account.html', title='account')
