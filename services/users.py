from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db



def login(username, password):
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()

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
    print("user_id", user_id)
    try:
        sql = "SELECT id, admin FROM users WHERE id=:user_id"
        result = db.session.execute(text(sql), {"user_id":user_id})
        admin = result.fetchone()[1]
        print("users", admin)
    except:
        print("except")
        return False

    return admin 

def logout():
    del session["username"]
    del session["user_id"]

def register(username, password, mail):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password,mail, created_at, last_modified, admin) VALUES (:username, :password, :mail, NOW(), NOW(), False)"
        db.session.execute(text(sql), {"username":username, "password":hash_value, "mail":mail})
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


def update_password(password, new_password, new_password2):
    #TSEKKAA OIKEELLISUUS!
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    username = session.get("username")
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    hash_value = user.password
    #password = request.form["password"]

    if check_password_hash(hash_value, password):
        
        #new_password = password
        #new_password2 = 
        hash_value = generate_password_hash(new_password)

        user_id = session.get("user_id")
        sql = "UPDATE users SET last_modified = NOW(), password=:new_password WHERE id=:user_id"
        db.session.execute(text(sql), {"new_password":hash_value, "user_id":user_id})
        db.session.commit()
        return True
    else: 
        return False


def get_created():
    pass
    
def feedback(feedback):
    user_id = session.get("user_id")
    sql = "INSERT INTO feedbacks (user_id, feedback, feedback_time) VALUES (:user_id, :feedback, NOW())"
    db.session.execute(text(sql), {"user_id": user_id, "feedback":feedback})
    db.session.commit()
