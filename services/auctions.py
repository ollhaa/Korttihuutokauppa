from flask import session
from sqlalchemy.sql import text
#from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def new(title, content, _class, condition, city, bid_start, ending_time):
    user_id = session.get("user_id")
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

def get_auction_facts():
    user_id = session.get("user_id")
    sql2 = "SELECT COUNT(*) FROM auctions WHERE user_id=:user_id"
    result2 = db.session.execute(text(sql2), {"user_id":user_id})
    num_of_messages = result2.fetchone()[0]

    sql3 = "SELECT COUNT(*) FROM bids WHERE user_id=:user_id"
    result3 = db.session.execute(text(sql3), {"user_id":user_id})
    num_of_bids = result3.fetchone()[0]

    return num_of_messages, num_of_bids