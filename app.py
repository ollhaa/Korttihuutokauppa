from os import getenv
from flask import Flask

app = Flask(__name__)
import routes

app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
