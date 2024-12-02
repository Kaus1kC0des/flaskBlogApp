from flask import render_template, redirect, flash, url_for, request
from flaskBlog import app, bcrypt, db
from flaskBlog.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os


posts = [
    {
        'title': 'First Post',
        'content': 'This is my first post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Second Post',
        'content': 'This is my second post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Third Post',
        'content': 'This is my third post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Fourth Post',
        'content': 'This is my fourth post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Fifth Post',
        'content': 'This is my fifth post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Sixth Post',
        'content': 'This is my sixth post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Seventh Post',
        'content': 'This is my seventh post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Eighth Post',
        'content': 'This is my eighth post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Ninth Post',
        'content': 'This is my ninth post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Tenth Post',
        'content': 'This is my tenth post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Eleventh Post',
        'content': 'This is my eleventh post',
        'author': 'Kausik',
        'date': '28/11/24'
    },
    {
        'title': 'Twelfth Post',
        'content': 'This is my twelfth post',
        'author': 'Kausik',
        'date': '2/12/24'
    },
    {
        'title': 'Thirteenth Post',
        'content': 'This is my thirteenth post',
        'author': 'Kausik',
        'date': '2/12/24'
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_format = os.path.splitext(form_picture.filename)
    picture_filename = random_hex+file_format
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_filename


@app.route('/account', methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_picture = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            os.remove(current_picture)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your account has been updated", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/"+current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


