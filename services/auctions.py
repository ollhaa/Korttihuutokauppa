from flask import session
from sqlalchemy.sql import text
#from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def new(title, content, _class, condition, city,data1, data2,name1, name2, bid_start, ending_time):
    user_id = session.get("user_id")
    if len(title.replace(" ", "")) < 5 or len(content.replace(" ", "")) < 10:
        return False

    try:
        sql1 = """INSERT INTO auctions (user_id, title, content, _class, condition, city, bid_start, created_at, ending_time, active, winner_id) \
        VALUES (:user_id, :title, :content, :_class, :condition, :city, :bid_start, NOW(), :ending_time, True, 0)"""
        db.session.execute(text(sql1), {"user_id":user_id, "title":title, "content":content, "_class":_class, "condition":condition, "city":city, \
        "bid_start":bid_start, "ending_time":ending_time, "winner_id":user_id})

        sql = "SELECT id FROM auctions ORDER BY id DESC LIMIT 1" 
        rows = db.session.execute(text(sql))
        if rows is None:
            auction_id = 1
        else: 
            auction_id = rows.fetchone()[0]

        sql2 = """INSERT INTO images (auction_id, name, data) VALUES (:auction_id, :name, :data)"""
        db.session.execute(text(sql2), {"auction_id":auction_id, "name":name1, "data":data1})

        sql3 = """INSERT INTO images (auction_id, name, data) VALUES (:auction_id, :name, :data)"""
        db.session.execute(text(sql3), {"auction_id":auction_id, "name":name2, "data":data2})

        db.session.commit()
    
    except:
        return False
    
    return True

def update_auctions():
    print("toimiiko")
    sql = """UPDATE auctions SET active = False WHERE ending_time < NOW()"""
    db.session.execute(text(sql))
    db.session.commit()

def update_winners():
    update_auctions()
    try:
        sql= "SELECT id,user_id FROM auctions WHERE winner_id != user_id AND solved = False"
        result = db.session.execute(text(sql))
        todo = result.fetchall()
        print("todo: ", todo)
        for x in todo:
            print("x:", x)
            sql1 = """UPDATE auctions SET winner_id = (SELECT user_id FROM bids GROUP BY auction_id WHERE bid = MAX(bid) AND auction_id =:x)"""
            db.session.execute(text(sql1),{"x":x[0]})

        
        sql2= "SELECT auctions.id, auctions.title, auctions.user_id, auctions.winner_id, users.mail FROM auctions, users \
        WHERE auctions.solved = False AND auctions.user_id = users.mail"
        db.session.excute(text(sql2))
        todo2 = result.fetchall()
        print("todo2: ", todo2 )
        for x in todo2:
            print("x: ", x)
            message = "Olet voittanut huutokaupan", x[0],":", x[1], "Voit ottaa yhteyttä mailiin: ", x[5]
            sql3 = """INSERT INTO messages (user_id_from, user_id_to, message, message_sent) VALUES (:user_id_from, :user_id_to, :message, NOW())"""
            db.session.execute(text(sql3),{"user_id_from":0, "user_id_to":x[3],"message":message})

        sql4 = """UPDATE auctions SET solved = True WHERE ending_time < NOW() AND solved = False"""
        db.session.execute(text(sql4))
        db.session.commit()
    except:
        return False
    return True

def get_auction_facts():
    user_id = session.get("user_id")
    sql2 = "SELECT COUNT(*) FROM auctions WHERE user_id=:user_id"
    result2 = db.session.execute(text(sql2), {"user_id":user_id})
    num_of_messages = result2.fetchone()[0]

    sql3 = "SELECT COUNT(*) FROM bids WHERE user_id=:user_id"
    result3 = db.session.execute(text(sql3), {"user_id":user_id})
    num_of_bids = result3.fetchone()[0]

    return num_of_messages, num_of_bids

def get_auction(id):
    sql = "SELECT * FROM auctions WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    auction = result.fetchall()[0]
    return auction

def get_auction_max_bid(id):
    sql2 = "SELECT b.bid, b.bid_time, u.username FROM bids b LEFT JOIN users u ON b.user_id=u.id WHERE b.auction_id=:auction_id AND b.bid = (SELECT MAX(bid) FROM bids)"
    result2 = db.session.execute(text(sql2),{"auction_id":id})
    max_bid = result2.fetchone()

    return max_bid

def result(_class, city, condition):
    #if _class is None or city is None or condition is None:
    #    return False

    if _class == "Kaikki" and city == "Kaikki" and condition == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True ORDER BY id DESC"
        result = db.session.execute(text(sql))

    elif  _class == "Kaikki" and city == "Kaikki":
        sql ="SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"condition":condition})
    elif _class == "Kaikki" and condition =="Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND city=:city ORDER BY id DESC"
        result = db.session.execute(text(sql), {"city":city})
    elif city =="Kaikki" and condition =="Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND _class=:_class ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class})

    elif _class == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND city=:city AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"city":city, "condition":condition})
    elif city == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND _class=:_class AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "condition":condition})
    elif condition == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND _class=:_class AND city=:city ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "city":city})

    else:
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time FROM auctions WHERE active=True AND _class=:_class AND city=:city AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "city":city, "condition":condition})

    auctions = result.fetchall()
    
    return auctions

def show_front(id):
    sql3 = "SELECT data FROM images WHERE auction_id=:auction_id"
    result3 = db.session.execute(text(sql3),{"auction_id":id})
    data = result3.fetchone()[0]
    return data

def show_back(id):
    sql3 = "SELECT data FROM images WHERE auction_id=:auction_id AND id=:apu"
    result3 = db.session.execute(text(sql3),{"auction_id":id, "apu":id+1})
    data = result3.fetchone()[0]
    return data

def make_bid(auction_id, user_id, bid):
    sql = "SELECT MAX(bid) FROM bids WHERE auction_id=:auction_id"
    result = db.session.execute(text(sql),{"auction_id":auction_id})
    max_price = result.fetchone()[0]
    sql2 = "SELECT bid_start FROM auctions WHERE id=:auction_id"
    result = db.session.execute(text(sql2),{"auction_id":auction_id})
    start_price = result.fetchone()[0]
    print("start_price", start_price)
    if max_price is None:
        new_price = int(start_price) + int(bid)
    else:
        new_price = int(max_price) + int(bid)

    sql = "SELECT active from auctions WHERE id=:auction_id"
    result = db.session.execute(text(sql),{"auction_id":auction_id})
    if result.fetchone()[0]:
        sql1 = """INSERT INTO bids (user_id, auction_id, bid, bid_time) VALUES (:user_id, :auction_id, :bid, NOW())"""
        db.session.execute(text(sql1), { "user_id":user_id, "auction_id":auction_id, "bid":new_price})

        db.session.commit()


