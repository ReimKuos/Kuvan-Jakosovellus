from operator import pos
from re import S
from db import db

def get_user_id(user_id: str):
    sql = "SELECT id FROM users WHERE user_id=:user_id"
    id = db.session.execute(sql, {"user_id": user_id})
    return id.fetchone()[0]

def get_group_info(group_id: int):
    sql = "SELECT group_name, description FROM groups WHERE id=:group_id"
    name = db.session.execute(sql, {"group_id": group_id})
    return name.fetchone()

def get_post_info(post_id: int):
    sql = "SELECT id, post_title FROM posts WHERE visible AND id=:post_id"
    info = db.session.execute(sql, {"post_id": post_id})
    return info.fetchone()

def check_like(post_id: int, user_id: int):
    sql = "SELECT active FROM likes WHERE post_id=:post_id AND liker_id=:user_id LIMIT 1"
    value = db.session.execute(sql, {"user_id":user_id, "post_id":post_id}).fetchone()
    return value if value is None else value[0]


def like_post(post_id: int, user_id: int):
    if check_like(post_id, user_id) is None:
        sql = "INSERT INTO likes (post_id, liker_id, active) VALUES (:post_id, :user_id, TRUE)"
    else:
        sql = "UPDATE likes SET active=TRUE WHERE post_id=:post_id AND liker_id=:user_id"
    try:
        db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
        db.session.commit()
        return True
    except:
        return False

def remove_like(post_id: int, user_id: int):
    if check_like(post_id, user_id) is None:
        sql = "INSERT INTO likes (post_id, liker_id, active) VALUES (:post_id, :user_id, FALSE)"
    else:
        sql = "UPDATE likes SET active=FALSE WHERE post_id=:post_id AND liker_id=:user_id"
    try:
        db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
        db.session.commit()
        return True
    except:
        return False
