from os import getenv
from flask import Flask, render_template, redirect, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///ohaapasa"
db = SQLAlchemy(app)

@app.route("/")
def index():
    if session.get("username"):
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="GET":
       return render_template("login.html")
    if request.method=="POST": 
        username = request.form["username"]
        password = request.form["password"]
        # TODO: tarkista sanat
        sql = "SELECT id, username, password FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username":username})
        user = result.fetchone()

        if not user:
            return render_template("login.html")
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = user.username
            session["user_id"] = user.id
            return redirect("/")
        else: 
            return render_template("login.html")

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

        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password,mail, created_at, last_modified, admin) VALUES (:username, :password, :mail, NOW(), NOW(), False)"
        db.session.execute(text(sql), {"username":username, "password":hash_value, "mail":mail})
        db.session.commit()
        return redirect("/login")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback", methods=["GET", "POST"])
def send_feedback():
    if request.method == "GET":
        return render_template("feedback.html")
    if request.method == "POST":
        feedback = request.form["feedback"]
        user_id = session.get("user_id")
        sql = "INSERT INTO feedbacks (user_id, feedback, feedback_time) VALUES (:user_id, :feedback, NOW())"
        db.session.execute(text(sql), {"user_id": user_id, "feedback":feedback})
        db.session.commit()
        return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        tomorrow = datetime.today() + timedelta(1)
        oneweek = datetime.today()+ timedelta(7)
        return render_template("new.html", tomorrow=tomorrow, oneweek=oneweek)
    if request.method == "POST":
        user_id = session.get("user_id")
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

        sql = "SELECT COUNT(*) FROM auctions" 
        rows = db.session.execute(text(sql))

        auction_id = rows.fetchone()[0] +1
        #print(auction_id)

        sql1 = "INSERT INTO auctions (user_id, title, content, _class, condition, city, bid_start, created_at, ending_time, active) \
        VALUES (:user_id, :title, :content, :_class, :condition, :city, :bid_start, NOW(), :ending_time, True)"
        db.session.execute(text(sql1), {"user_id":user_id, "title":title, "content":content, "_class":_class, "condition":condition, "city":city, \
        "bid_start":bid_start, "ending_time":ending_time})

        sql2 = "INSERT INTO images (auction_id, name, data) VALUES (:auction_id, :name, :data)"
        db.session.execute(text(sql2), {"auction_id":auction_id, "name":name1, "data":data1})

        sql3 = "INSERT INTO images (auction_id, name, data) VALUES (:auction_id, :name, :data)"
        db.session.execute(text(sql3), {"auction_id":auction_id, "name":name2, "data":data2})


        db.session.commit()
        return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        user_id = session.get("user_id")
        sql = "SELECT username, created_at FROM users WHERE id=:user_id"
        result1 = db.session.execute(text(sql), {"user_id":user_id})
        facts = result1.fetchone()

        sql2 = "SELECT COUNT(*) FROM auctions WHERE user_id=:user_id"
        result2 = db.session.execute(text(sql2), {"user_id":user_id})
        num_of_messages = result2.fetchone()[0]

        sql3 = "SELECT COUNT(*) FROM bids WHERE user_id=:user_id"
        result3 = db.session.execute(text(sql3), {"user_id":user_id})
        num_of_bids = result3.fetchone()[0]

        return render_template("profile.html", facts=facts, num_of_messages=num_of_messages, num_of_bids=num_of_bids)
    
    if request.method == "POST":
        sql = "SELECT id, username, password FROM users WHERE username=:username"
        username = session.get("username")
        result = db.session.execute(text(sql), {"username":username})
        user = result.fetchone()
        hash_value = user.password
        password = request.form["password"]

        if check_password_hash(hash_value, password):
            
            new_password = request.form["new_password"]
            new_password2 = request.form["new_password2"]

            hash_value = generate_password_hash(new_password)

            user_id = session.get("user_id")
            sql = "UPDATE users SET last_modified = NOW(), password=:new_password WHERE id=:user_id"
            db.session.execute(text(sql), {"new_password":hash_value, "user_id":user_id})
            db.session.commit()
            return redirect("/")
        else:
            return render_template("/logout")


@app.route("/search")
def search():
    return render_template("search.html")
    

@app.route("/results", methods=["POST"])
def results():
    _class = request.form["_class"]
    print(_class)
    city = request.form["city"]
    condition = request.form["condition"]

    if _class is None or city is None or condition is None:
        return redirect("/search")

    if _class == "Kaikki" and city == "Kaikki" and condition == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions ORDER BY id DESC"
        result = db.session.execute(text(sql))
    elif  _class == "Kaikki" and city == "Kaikki":
        sql ="SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"condition":condition})
    elif _class == "Kaikki" and condition =="Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE city=:city ORDER BY id DESC"
        result = db.session.execute(text(sql), {"city":city})
    elif city =="Kaikki" and condition =="Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE _class=:_class ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class})

    elif _class == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE city=:city AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"city":city, "condition":condition})
    elif city == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE _class=:_class AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "condition":condition})
    elif condition == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE _class=:_class AND city=:city ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "city":city})

    else:
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE _class=:_class AND city=:city AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "city":city, "condition":condition})


    auctions = result.fetchall()
    return render_template("results.html", auctions=auctions)


@app.route("/auction/<int:id>", methods=["GET"])
def auction(id):
    if request.method=="GET":
        sql = "SELECT * FROM auctions WHERE id=:id"
        result = db.session.execute(text(sql), {"id":id})
        auction = result.fetchall()[0]

        sql2 = "SELECT b.bid, b.bid_time, u.username FROM bids b LEFT JOIN users u ON b.user_id=u.id WHERE b.auction_id=:auction_id AND b.bid = (SELECT MAX(bid) FROM bids)"
        result2 = db.session.execute(text(sql2),{"auction_id":id})
        max_bid = result2.fetchone()
 
        return render_template("auction.html",id=id, auction=auction, max_bid=max_bid)

@app.route("/show_front/<int:id>")
def show_front(id):
    sql3 = "SELECT data FROM images WHERE auction_id=:auction_id"
    result3 = db.session.execute(text(sql3),{"auction_id":id})
    data = result3.fetchone()[0]
    #print(data)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/show_back/<int:id>")
def show_back(id):
    sql3 = "SELECT data FROM images WHERE auction_id=:auction_id AND id=:apu"
    result3 = db.session.execute(text(sql3),{"auction_id":id, "apu":id+1})
    data = result3.fetchone()[0]
    #print(data)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/bid", methods= ["POST"])
def bid():
    #request.method=="POST":
    bid = request.form["bid"]
    print(bid)
    auction_id =request.form["auction_id"]
    user_id = session.get("user_id")

    sql = "SELECT MAX(bid) FROM bids WHERE auction_id=:auction_id"
    result = db.session.execute(text(sql),{"auction_id":auction_id})
    max_price = result.fetchone()[0]
    if max_price is None:
        new_price = bid
    else:
        new_price = int(max_price) + int(bid)

    sql1 = "INSERT INTO bids (user_id, auction_id, bid, bid_time) VALUES (:user_id, :auction_id, :bid, NOW())"
    db.session.execute(text(sql1), { "user_id":user_id, "auction_id":auction_id, "bid":new_price})

    db.session.commit()
    return redirect("/")
