from os import getenv
from flask import Flask, render_template, redirect, request, session, make_response
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import text
#from datetime import datetime, timedelta
#from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask
#from services import users

app = Flask(__name__)

import routes
app.secret_key = getenv("SECRET_KEY")
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///ohaapasa"
uri = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
#db = SQLAlchemy(app)

