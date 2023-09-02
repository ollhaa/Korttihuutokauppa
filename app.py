from os import getenv
from flask import Flask, render_template, redirect, request, session, make_response
#from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
import routes
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")



scheduler = BackgroundScheduler()
job= scheduler.add_job(routes.test_job, "interval", minutes=1)
scheduler.start()
