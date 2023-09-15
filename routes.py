from datetime import datetime, timedelta
from flask import render_template, redirect, request, make_response, flash
from app import app
from services import users
from services import auctions


@app.route("/")
def index():
    if users.is_logged():
        user = users.is_logged()
        username = user[0:3]+"..."
        admin_rights = users.is_admin()
        return render_template("index.html", username= username, admin=admin_rights)
    return render_template("/login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            flash("Salasana tai käyttäjätunnus väärin!")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method=="POST":
        users.check_csrf()
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        mail = request.form["mail"]
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
        if not users.register(username, password, mail):
            flash("Käyttäjä on jo olemassa tai jokin muu virhe")
            return render_template("/register.html")
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
        admin_rights = users.is_admin()
        return render_template("feedback.html", username= username, admin=admin_rights)
    if request.method == "POST":
        users.check_csrf()
        feedback = request.form["feedback"]
        if len(feedback) > 120:
            flash("Palautteen maksimimerkkimäärä on 120")
        if not users.feedback(feedback):
            flash("Palautteen antaminen ei onnistunut")
        else:
            flash("Palautteen antaminen onnistui!")
        return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    admin_rights = users.is_admin()
    if request.method == "GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin_rights = users.is_admin()
        tomorrow = datetime.today() + timedelta(1)
        oneweek = datetime.today()+ timedelta(7)
        return render_template("new.html", tomorrow=tomorrow, oneweek=oneweek,
        username= username, admin=admin_rights)

    if request.method == "POST":
        users.check_csrf()
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
        if len(data1) > 1000*1024:
            flash("Liian suuri tiedosto")
            return render_template("/new.html")
        file2 = request.files["file2"]
        name2 = file2.filename
        if not name2.endswith(".jpg"):
            flash("Väärä tiedostomuoto!")
            return render_template("/new.html")
        data2 = file2.read()
        if len(data2) > 1000*1024:
            flash("Liian suuri tiedosto")
            return render_template("/new.html")
        bid_start = request.form["bid_start"]
        ending_time = request.form["ending_time"]

        if not auctions.new(title, content, _class, condition, city,
         data1, data2, name1, name2, bid_start, ending_time):
            flash("Tallennus ei onnistunut")
            return redirect("/new")
        flash("Tallennus onnistui!")
        return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    admin_rights = users.is_admin()
    if request.method == "GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin_rights = users.is_admin()
        facts = users.get_profile_facts()
        num_of_messages, num_of_bids = auctions.get_auction_facts()
        return render_template("profile.html",
        facts=facts, num_of_messages=num_of_messages,
        num_of_bids=num_of_bids, username= username, admin=admin_rights)
    if request.method == "POST":
        users.check_csrf()
        password = request.form["password"]
        new_password = request.form["new_password"]
        new_password2 = request.form["new_password2"]
        if len(new_password) <4 or len(new_password) >10:
            flash("Salasanan vaihtoepäonnistui! Tarkista uuden salasanan pituus")
        if new_password != new_password2:
            flash("Salasanan vaihto epäonnistui! Salasanat eivät ole samat")

        if users.update_password(password, new_password):
            flash("Salasana vaihdettu")
            return redirect("/")

    return redirect("/logout")

@app.route("/search")
def search():
    user = users.is_logged()
    username = user[0:3]+"..."
    admin_rights = users.is_admin()
    auctions.update_auctions()
    return render_template("search.html", username= username, admin=admin_rights)

@app.route("/results", methods=["POST"])
def results():
    users.check_csrf()
    user = users.is_logged()
    username = user[0:3]+"..."
    admin_rights = users.is_admin()
    _class = request.form["_class"]
    city = request.form["city"]
    condition = request.form["condition"]

    if _class is None or city is None or condition is None:
        return redirect("/search")
    auctions.update_auctions()
    open_auctions = auctions.results(_class, city, condition)
    return render_template("results.html", auctions=open_auctions,
    username= username, admin=admin_rights)

@app.route("/auction/<int:id_>", methods=["GET"])
def auction(id_):
    admin_rights = users.is_admin()
    if request.method=="GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin_rights = users.is_admin()
        auction_ = auctions.get_auction(id_)
        max_bid = auctions.get_auction_max_bid(id_)
        return render_template("auction.html",id=id_,
        auction=auction_, max_bid=max_bid, username= username, admin=admin_rights)

@app.route("/show_front/<int:id_>")
def show_front(id_):
    data = auctions.show_front(id_)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/show_back/<int:id_>")
def show_back(id_):
    data = auctions.show_back(id_)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/bid", methods= ["POST"])
def bid():
    users.check_csrf()
    auctions.update_auctions()
    bid_ = request.form["bid"]
    auction_id =request.form["auction_id"]
    #TSEKKAA KOROTUS
    if auctions.make_bid(auction_id, bid_):
        flash("Korotus onnistui!")
    else:
        flash("Korotus epäonnistui tai yritit osallistua tekemääsi huutokauppaan!")
    return redirect("/")

@app.route("/messages", methods=["GET"])
def messages():
    if request.method=="GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin_rights = users.is_admin()
        user_messages = users.get_last_messages()
        return render_template("/messages.html",
        username= username, admin=admin_rights, messages= user_messages)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method=="GET":
        user = users.is_logged()
        username = user[0:3]+"..."
        admin_rights = users.is_admin()
        if admin_rights:
            return render_template("/admin.html", username= username, admin=admin_rights)
        flash("Ei oikeuksia")
        return render_template("/")
    if request.method=="POST":
        users.check_csrf()
        if request.form.get("id","") =="0":
            if not auctions.update_auctions():
                flash("Päivittäminen epäonnistui")
                return redirect("/admin")
            if not auctions.update_winners():
                flash("Päivittäminen epäonnistui2")
                return redirect("/admin")
            if not auctions.update_final():
                flash("Päivittäminen epäonnistui3")
                return redirect("/admin")
            flash("Päivittäminen onnistui!")
            return redirect("/")

        if request.form.get("id","") =="1":
            username = request.form["username"]
            password = request.form["password"]
            if not users.add_admin_rights(username, password):
                flash("Oikeuksien lisääminen epäonnistui")
                return redirect("/admin")
            flash("Oikeudet lisättty!")
            return redirect("/")

        if request.form.get("id","") =="2":
            username = request.form["username"]
            message = request.form["message"]
            #TSEKKAA VIESTIN PITUUS
            if not users.send_message(username, message):
                flash("Viestin lähettäminen epäonnistui")
                return redirect("/admin")
            flash("Viesti lähetetty!")
            return redirect("/")
                