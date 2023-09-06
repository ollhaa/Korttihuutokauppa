from app import app
from services import users
from services import auctions
from flask import Flask, render_template, redirect, request, session, make_response, flash
from datetime import datetime, timedelta

def test_job():
    users.test()
    #auctions.update_auctions()

@app.route("/")
def index():
    if users.is_logged():
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        #print("route",admin)
        return render_template("index.html", username= username, admin=admin)
    else:
        return render_template("/login.html")

@app.route("/logout")
def logout():
    if auctions.update_winners():
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
        if len(username) <4 or len(username) >10:
            flash("Tarkista nimen pituus")
            return render_template("/register.html")
        if len(password) <4 or len(password) >10:
            flash("Tarkista salasanan pituus")
            return render_template("/register.html")
        if password != password2:
            flash("Salasanat eivät ole samat")
            return render_template("/register.html")
        if "@" not in mail:
            flash("Sähköpostiosoite ei ole OK")
            return render_template("/register.html")
        #print("route:", users.register(username, password, mail))
        if not users.register(username, password, mail):
            flash("Käyttäjä on jo olemassa tai jokin muu virhe")
            return render_template("/register.html")
        else:
            flash("Rekisteröinti onnistui")
            return redirect("/login")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback", methods=["GET", "POST"])
def send_feedback():
    if request.method == "GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        return render_template("feedback.html", username= username, admin=admin)
    if request.method == "POST":
        feedback = request.form["feedback"]
        users.feedback(feedback)
        return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    admin = users.is_admin()
    if request.method == "GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        tomorrow = datetime.today() - timedelta(1)
        oneweek = datetime.today()+ timedelta(7)
        return render_template("new.html", tomorrow=tomorrow, oneweek=oneweek, username= username, admin=admin)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        _class = request.form["_class"]
        condition = request.form["condition"]
        city = request.form["city"]
        file1 = request.files["file1"]
        name1 = file1.filename
        if not name1.endswith(".jpg"):
            flash("Väärä tiedostomuoto!")
            return render_template("/new.html")
        data1 = file1.read()
        print(len(data1))
        if len(data1) > 1000*1024:
            flash("Liian suuri tiedosto")
            return render_template("/new.html")
        file2 = request.files["file2"]
        name2 = file2.filename
        if not name2.endswith(".jpg"):
            flash("Väärä tiedostomuoto!")
            return render_template("/new.html")
        data2 = file2.read()
        print(len(data2))
        if len(data2) > 1000*1024:
            flash("Liian suuri tiedosto")
            return render_template("/new.html")
        bid_start = request.form["bid_start"]
        ending_time = request.form["ending_time"]

        if not auctions.new(title, content, _class, condition, city,data1, data2,name1, name2, bid_start, ending_time):
            flash("Tallennus ei onnistunut")
            return render_template("/new.html")
        
        flash("Tallennus onnistui!")
        return redirect("/")
            
            
            



@app.route("/profile", methods=["GET", "POST"])
def profile():
    admin = users.is_admin()
    if request.method == "GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        facts = users.get_profile_facts()
        num_of_messages, num_of_bids = auctions.get_auction_facts()

        return render_template("profile.html", facts=facts, num_of_messages=num_of_messages, num_of_bids=num_of_bids, username= username, admin=admin)
    
    if request.method == "POST":
        password = request.form["password"]
            
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password2"]

        if users.update_password(password, new_password):
            flash("Salasana vaihdettu")
            return redirect("/")

    return redirect("/logout")


@app.route("/search")
def search():
    user = users.is_logged()
    username = user[0:3]+"..."
    admin = users.is_admin()
    auctions.update_auctions()
    return render_template("search.html", username= username, admin=admin)
    

@app.route("/results", methods=["POST"])
def results():
    user = users.is_logged()
    username = user[0:3]+"..."
    admin = users.is_admin()
    _class = request.form["_class"]
    city = request.form["city"]
    condition = request.form["condition"]

    if _class is None or city is None or condition is None:
        return redirect("/search")
    else: 
        auctions.update_auctions()
        open_auctions = auctions.result(_class, city, condition)
        return render_template("results.html", auctions=open_auctions, username= username, admin=admin)


@app.route("/auction/<int:id>", methods=["GET"])
def auction(id):
    admin = users.is_admin()
    if request.method=="GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        auction = auctions.get_auction(id)
        max_bid = auctions.get_auction_max_bid(id)
 
        return render_template("auction.html",id=id, auction=auction, max_bid=max_bid, username= username, admin=admin)

@app.route("/show_front/<int:id>")
def show_front(id):
    data = auctions.show_front(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/show_back/<int:id>")
def show_back(id):
    data = auctions.show_back(id)
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

@app.route("/messages", methods=["GET"])
def messages():
    if request.method=="GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        messages = users.get_last_messages()
        print(messages)
        return render_template("/messages.html", username= username, admin=admin, messages= messages)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method=="GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin = users.is_admin()
        if admin:
            return render_template("/admin.html", username= username, admin=admin)
        else:
            flash("Ei oikeuksia")
            return render_template("/")
    if request.method=="POST":
        #print("tättähäärää!")
        #print(request.args.get("id"))
        if request.form.get("id","") =="0":
            print("0")
            if not auctions.update_auctions():
                flash("Päivittäminen epäonnistui")
                return redirect("/admin")
            elif not auctions.update_winners():
                flash("Päivittäminen epäonnistui3")
            elif not auctions.update_final():
                flash("Päivittäminen epäonnistui2")
                return redirect("/admin")
            else:
                flash("Päivittäminen onnistui!")
                return redirect("/")
            

        if request.form.get("id","") =="1":
            print("1")
            username = request.form["username"]
            password = request.form["password"]
            if not users.add_admin_rights(username, password):
                flash("Oikeuksien lisääminen epäonnistui")
                return redirect("/admin")
            else:
            #if users.add_admin_rights(username, password):
                flash("Oikeudet lisättty!")
                return redirect("/")
                

            #return redirect("/")
        if request.form.get("id","") =="2":
            print("2")
            username = request.form["username"]
            message = request.form["message"]
            if not users.send_message(username, message):
                flash("Viestin lähettäminen epäonnistui")
                return redirect("/admin")
            else:
                #users.send_message(username, message):
                flash("Viesti lähetetty!")
                return redirect("/")
            
                


