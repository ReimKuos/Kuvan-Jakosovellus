from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def sign_in(user_id, password):
    sql = "SELECT id, password FROM users WHERE user_id=:user_id"
    user = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if user is None:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        return True
    return False


def create_new_user(name, user_id, password):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (name, user_id, password) VALUES (:name, :user_id, :password)"
        db.session.execute(sql, {"name":name, "user_id":user_id, "password": hash_value})
        db.session.commit()
        return True
    except:
        return False