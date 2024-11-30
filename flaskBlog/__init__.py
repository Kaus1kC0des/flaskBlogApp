from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

from flaskBlog import routes
