



def login(username, password):
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()

    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = user.username
        session["user_id"] = user.id
    return True

def is_logged():
    return session["user_name"]

def logout():
    del session["username"]
    del session["user_id"]

def register():
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password,mail, created_at, last_modified, admin) VALUES (:username, :password, :mail, NOW(), NOW(), False)"
    db.session.execute(text(sql), {"username":username, "password":hash_value, "mail":mail})
    db.session.commit()

def update_password():
    pass


def get_created():
    

