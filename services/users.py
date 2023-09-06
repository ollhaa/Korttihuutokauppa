from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db



def login(username, password):
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user.username =="Admin":
        session["username"] = user.username
        session["user_id"] = user.id
        return True
    if not user:
        return False
    hash_value = user.password
    if not check_password_hash(hash_value, password):
        return False
    else:
        session["username"] = user.username
        session["user_id"] = user.id
    return True

def is_logged():
    return session.get("username")

def is_admin():
    user_id = session.get("user_id")
    #print("user_id", user_id)
    try:
        sql = "SELECT id, admin FROM users WHERE id=:user_id"
        result = db.session.execute(text(sql), {"user_id":user_id})
        admin = result.fetchone()[1]
        #print("users", admin)
    except:
        #print("except")
        return False

    return admin 

def add_admin_rights(to_username, password):
    sql = "SELECT id, password, admin FROM users WHERE id=:user_id"
    user_id = session.get("user_id")
    result = db.session.execute(text(sql), {"user_id":user_id})
    user = result.fetchone()
    hash_value = user.password

    if not check_password_hash(hash_value, password) and user.admin ==False:
        return False

    else: 
        try: 
            #print("try")
            sql = "SELECT id, username, admin FROM users WHERE username=:to_username"
            #username = session.get("username")
            result = db.session.execute(text(sql), {"to_username":to_username})
            user = result.fetchone()
            #print("user", user)
            #print("user.admin", user.admin)
            if user.admin == True:
                return False
            else:
                sql2 = """UPDATE users SET last_modified = NOW(), admin = True WHERE id =:to_user_id"""
                #print("user_id", user.id)
                db.session.execute(text(sql2), {"to_user_id":user.id})
                db.session.commit()
                #print("commit")
                return True
        except:
            #print("except")
            return False
            
        
    

def send_message(username, message):
    if username == session.get("username"):
        return False
    
    try:
        user_id_from = session.get("user_id")
        sql = "SELECT id, username FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username":username})
        #print("fetch_hone: ", result.fetchone())
        user_id_to = result.fetchone()[0]
        #print("user_id_to", user_id_to)
        sql2 = """INSERT INTO messages (user_id_from, user_id_to, message, message_sent) VALUES (:user_id_from, :user_id_to, :message, NOW())"""
        db.session.execute(text(sql2), {"user_id_from":user_id_from, "user_id_to":user_id_to, "message":message})
        db.session.commit()
    except:
        return False

    return True

def get_last_messages():
    user_id_to = session.get("user_id")
    sql = "SELECT message, message_sent FROM messages WHERE user_id_to=:user_id_to"
    result = db.session.execute(text(sql), {"user_id_to":user_id_to})
    #print("result", result)
    messages = result.fetchall()
    #print(messages)
    return messages


def logout():
    del session["username"]
    del session["user_id"]

def register(username, password, mail):
    
    sql = "SELECT username, password, mail FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    #print("result", result)
    user = result.fetchone()
    #print("user", user)
    #print("user vrt",  user is not None)
    if user is not None:
        #print("eka")
        return False
        #print("toka")
    
    hash_value = generate_password_hash(password)
    try:
        sql2 = """INSERT INTO users (username, password,mail, created_at, last_modified, admin) VALUES (:username, :password, :mail, NOW(), NOW(), False)"""
        db.session.execute(text(sql2), {"username":username, "password":hash_value, "mail":mail})
        db.session.commit()
    except:
        return False
    
    return True

def get_profile_facts():
    user_id = session.get("user_id")
    sql = "SELECT username, created_at FROM users WHERE id=:user_id"
    result1 = db.session.execute(text(sql), {"user_id":user_id})
    facts = result1.fetchone()

    return facts


def update_password(password, new_password):
    #TSEKKAA OIKEELLISUUS!
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    username = session.get("username")
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    hash_value = user.password
    #password = request.form["password"]

    if not check_password_hash(hash_value, password):
        return False
    try:
        hash_value = generate_password_hash(new_password)

        user_id = session.get("user_id")
        sql = """UPDATE users SET last_modified = NOW(), password=:new_password WHERE id=:user_id"""
        db.session.execute(text(sql), {"new_password":hash_value, "user_id":user_id})
        db.session.commit()
    except:
        False
    
    return True


    
def feedback(feedback):
    user_id = session.get("user_id")
    sql = """INSERT INTO feedbacks (user_id, feedback, feedback_time) VALUES (:user_id, :feedback, NOW())"""
    db.session.execute(text(sql), {"user_id": user_id, "feedback":feedback})
    db.session.commit()


def test():
    print("tata")
