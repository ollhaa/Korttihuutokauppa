from app import app
from services import users
from services import auctions
from flask import Flask, render_template, redirect, request, session, make_response, flash
from datetime import datetime, timedelta

@app.route("/")
def index():
    if users.is_logged():
        return render_template("index.html")
    else:
        return render_template("/login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method =="GET":
       return render_template("login.html")
    if request.method=="POST": 
        username = request.form["username"]
        password = request.form["password"]
        # TODO: tarkista sanat

        if not users.login(username, password):
            #flash("Salasana ja käyttäjätunnus OK")
            error = "Salasana tai käyttäjätunnus väärin!"
            flash(error)

        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        mail = request.form["mail"]
        # TODO: tarkista sanat
        if len(username) <4 or len(username) >12:
            flash("Tarkista nimen pituus")
            return render_template("/register.html")
        if len(password) <4 or len(password) >12:
            flash("Tarkista salasanan pituus")
        if password != password2:
            flash("Salasanat eivät ole samat")
        if "@" not in mail:
            flash("Sähköpostiosoite ei ole OK")
        
        if users.register(username, password, mail) == False:
            flash("Käyttäjä on jo olemassa ja jokin muu virhe")
        else:
            flash("Rekisteröinti onnistui")
            return render_template("/login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback", methods=["GET", "POST"])
def send_feedback():
    if request.method == "GET":
        return render_template("feedback.html")
    if request.method == "POST":
        feedback = request.form["feedback"]
        users.feedback(feedback)
        return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        tomorrow = datetime.today() + timedelta(1)
        oneweek = datetime.today()+ timedelta(7)
        return render_template("new.html", tomorrow=tomorrow, oneweek=oneweek)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        _class = request.form["_class"]
        condition = request.form["condition"]
        city = request.form["city"]
        file1 = request.files["file1"]
        name1 = file1.filename
        data1 = file1.read()
        file2 = request.files["file2"]
        name2 = file2.filename
        data2 = file2.read()
        bid_start = request.form["bid_start"]
        ending_time = request.form["ending_time"]

        auctions.new(title, content, _class, condition, city,data1, data2,name1, name2, bid_start, ending_time)
        return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        facts = users.get_profile_facts()
        num_of_messages, num_of_bids = auctions.get_auction_facts()

        return render_template("profile.html", facts=facts, num_of_messages=num_of_messages, num_of_bids=num_of_bids)
    
    if request.method == "POST":
        password = request.form["password"]
            
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password2"]

        if users.update_password(password, new_password, new_password2):
                return redirect("/")

    return render_template("/logout")


@app.route("/search")
def search():
    auctions.update_auctions()
    return render_template("search.html")
    

@app.route("/results", methods=["POST"])
def results():
    _class = request.form["_class"]
    city = request.form["city"]
    condition = request.form["condition"]

    if _class is None or city is None or condition is None:
        return redirect("/search")
    else: 
        auctions.update_auctions()
        open_auctions = auctions.result(_class, city, condition)
        return render_template("results.html", auctions=open_auctions)


@app.route("/auction/<int:id>", methods=["GET"])
def auction(id):
    if request.method=="GET":
        auction = auctions.get_auction(id)
        max_bid = auctions.get_auction_max_bid(id)
 
        return render_template("auction.html",id=id, auction=auction, max_bid=max_bid)

@app.route("/show_front/<int:id>")
def show_front(id):
    data = auctions.show_front(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/show_back/<int:id>")
def show_back(id):
    data = auctions.show_front(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/bid", methods= ["POST"])
def bid():
    auctions.update_auctions()
    bid = request.form["bid"]
    auction_id =request.form["auction_id"]
    user_id = session.get("user_id")

    auctions.make_bid(auction_id, user_id, bid)
    return redirect("/")
