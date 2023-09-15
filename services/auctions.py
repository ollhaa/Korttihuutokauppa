from flask import session
from sqlalchemy.sql import text
from db import db

def new(title, content, _class, condition, city,data1, data2,name1, name2, bid_start, ending_time):
    user_id = session.get("user_id")
    if len(title) < 5 or len(content) < 10:
        return False
    try:
        sql1 = """INSERT INTO auctions (user_id, title, content, _class, condition,\
        city, bid_start, created_at, ending_time, active, winner_id) \
        VALUES (:user_id, :title, :content, :_class, :condition, :city, :bid_start,\
        NOW(), :ending_time, True, :winner_id)"""
        db.session.execute(text(sql1), {"user_id":user_id, "title":title, "content":content, \
        "_class":_class, "condition":condition, "city":city,\
        "bid_start":bid_start, "ending_time":ending_time, "winner_id":user_id})

        sql = "SELECT id FROM auctions WHERE title =:title"
        rows = db.session.execute(text(sql), {"title":title})
        auction_id = rows.fetchone()[0]
        sql2 = """INSERT INTO images (auction_id, name,frontside, data)\
        VALUES (:auction_id, :name, :frontside, :data)"""
        db.session.execute(text(sql2), {"auction_id":auction_id, "name":name1,\
        "frontside":True, "data":data1})
        sql3 = """INSERT INTO images (auction_id, name, frontside, data)\
        VALUES (:auction_id, :name, :frontside, :data)"""
        db.session.execute(text(sql3), {"auction_id":auction_id, "name":name2,\
        "frontside":False, "data":data2})
        db.session.commit()
    except:
        return False
    return True

def update_auctions():
    try:
        sql = """UPDATE auctions SET active = False WHERE ending_time < NOW()"""
        db.session.execute(text(sql))
        db.session.commit()
    except:
        return False
    return True

def update_winners():
    try:
        sql= "SELECT id,user_id FROM auctions WHERE active = False AND solved = False"
        result = db.session.execute(text(sql))
        todos = result.fetchall()
        if len(todos) == 0:
            return True
        for todo in todos:
            sql1 = """UPDATE auctions SET winner_id = COALESCE((SELECT user_id FROM bids \
            WHERE auction_id =:x  ORDER BY bid DESC LIMIT 1),:user_id) WHERE id =:id"""
            db.session.execute(text(sql1),{"x":todo[0],"user_id":todo[1], "id":todo[0]})
        db.session.commit()
    except:
        return False
    return True

def update_final():
    try:
        sql2= "SELECT auctions.id, auctions.title, auctions.user_id, auctions.winner_id, \
        users.mail FROM auctions, users WHERE auctions.solved = False AND auctions.active = False \
        AND auctions.user_id = users.id"
        result = db.session.execute(text(sql2))
        todos = result.fetchall()
        if len(todos) == 0:
            return True
        for todo in todos:
            admin =1
            message = "Olet voittanut huutokaupan " + str(todo[0]) + ": " + str(todo[1]) + \
             " (tai se on aloittamasi). Voit nyt ottaa yhteyttä mailiin: " + str(todo[4]) +"."
            sql3 = """INSERT INTO messages (user_id_from, user_id_to, message, message_sent) \
            VALUES (:user_id_from, :user_id_to, :message, NOW())"""
            db.session.execute(text(sql3), \
            {"user_id_from":admin, "user_id_to":todo[3], "message":message})
            message2 = "Tekemäsi huutokauppa on päättynyt"
            sql4 = """INSERT INTO messages (user_id_from, user_id_to, message, message_sent) \
            VALUES (:user_id_from, :user_id_to, :message, NOW())"""
            db.session.execute(text(sql4),{"user_id_from":admin, \
            "user_id_to":todo[2],"message":message2})
        #print("täällä?")
        sql5 = """UPDATE auctions SET solved = True WHERE ending_time < NOW() AND solved = False"""
        db.session.execute(text(sql5))
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

def get_auction(id_):
    sql = "SELECT * FROM auctions WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id_})
    auction = result.fetchall()[0]
    return auction

def get_auction_max_bid(id_):
    sql2 = "SELECT b.bid, b.bid_time, u.username FROM bids b LEFT JOIN users u ON b.user_id=u.id \
    WHERE b.auction_id=:auction_id AND b.bid = (SELECT MAX(bid) FROM bids)"
    result2 = db.session.execute(text(sql2),{"auction_id":id_})
    max_bid = result2.fetchone()

    return max_bid

def results(_class, city, condition):
    if _class == "Kaikki" and city == "Kaikki" and condition == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, \
        ending_time FROM auctions WHERE active=True ORDER BY id DESC"
        result = db.session.execute(text(sql))
    elif  _class == "Kaikki" and city == "Kaikki":
        sql ="SELECT id, title,content, _class,condition, city, bid_start, created_at, ending_time \
        FROM auctions WHERE active=True AND condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"condition":condition})
    elif _class == "Kaikki" and condition =="Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at,\
        ending_time FROM auctions WHERE active=True AND city=:city ORDER BY id DESC"
        result = db.session.execute(text(sql), {"city":city})
    elif city =="Kaikki" and condition =="Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at,\
        ending_time FROM auctions WHERE active=True AND _class=:_class ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class})
    elif _class == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at,\
        ending_time FROM auctions WHERE active=True AND city=:city AND condition=:condition \
          BY id DESC"
        result = db.session.execute(text(sql), {"city":city, "condition":condition})
    elif city == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at,\
        ending_time FROM auctions WHERE active=True AND _class=:_class AND \
        condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "condition":condition})
    elif condition == "Kaikki":
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, \
        ending_time FROM auctions WHERE active=True AND _class=:_class AND city=:city \
        ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "city":city})
    else:
        sql = "SELECT id, title,content, _class,condition, city, bid_start, created_at, \
        ending_time FROM auctions WHERE active=True AND _class=:_class AND city=:city AND \
        condition=:condition ORDER BY id DESC"
        result = db.session.execute(text(sql), {"_class":_class, "city":city, \
        "condition":condition})
    auctions = result.fetchall()
    return auctions

def show_front(id_):
    sql3 = "SELECT data FROM images WHERE auction_id=:auction_id AND \
    frontside=:frontside"
    result3 = db.session.execute(text(sql3),{"auction_id":id_, "frontside":True})
    data = result3.fetchone()[0]
    return data

def show_back(id_):
    sql3 = "SELECT data FROM images WHERE auction_id=:auction_id AND frontside=:frontside"
    result3 = db.session.execute(text(sql3),{"auction_id":id_, "frontside":False})
    data = result3.fetchone()[0]
    return data

def make_bid(auction_id, bid):
    user_id = session.get("user_id")
    try:
        sql = "SELECT MAX(bid) FROM bids WHERE auction_id=:auction_id"
        result = db.session.execute(text(sql),{"auction_id":auction_id})
        max_price = result.fetchone()[0]
        sql = "SELECT bid_start FROM auctions WHERE id=:auction_id"
        result = db.session.execute(text(sql),{"auction_id":auction_id})
        start_price = result.fetchone()[0]
        if max_price is None:
            new_price = int(start_price) + int(bid)
        else:
            new_price = int(max_price) + int(bid)
        sql = "SELECT active from auctions WHERE id=:auction_id AND user_id !=:user_id"
        result = db.session.execute(text(sql),{"auction_id":auction_id, "user_id":user_id})
        if len(result.fetchone()) == 0:
            return False
        sql = """INSERT INTO bids (user_id, auction_id, bid, bid_time) \
        VALUES (:user_id, :auction_id, :bid, NOW())"""
        db.session.execute(text(sql), { "user_id":user_id, "auction_id":auction_id, \
        "bid":new_price})
        db.session.commit()
    except:
        return False

    return True
