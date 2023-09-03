from os import getenv
from flask import Flask, render_template, redirect, request, session, make_response
#from flask import Flask
from flask_apscheduler import APScheduler

#from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
import routes
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

scheduler = APScheduler()
def your_task():
    app = apscheduler.app
    with app.app_context():
        users = routes.test_job()

scheduler.init_app(app)
scheduler.start()



#job= scheduler.add_job(routes.test_job, "interval", minutes=1)
#scheduler.start()
