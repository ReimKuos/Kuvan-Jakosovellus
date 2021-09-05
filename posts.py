from werkzeug import datastructures
from db import db

def create_new_post(creator_id: int, group_id: int, post_title: str, picture):
    sql = "INSERT INTO posts (creator_id, group_id, creation_time, visible, removed, post_title, picture)" \
          "VALUES (:creator_id, :group_id, NOW(), TRUE, FALSE, :post_title, :picture)"
    db.session.execute(sql, {"creator_id": creator_id, "group_id": group_id, "post_title": post_title, "picture": picture})
    db.session.commit()
    return True


def save_image(picture):
    name = picture.filename
    if  not name.endswith(".jpg"):
        return "Photo must be in jpg fromat"
    data = picture.read()
    if len(data) > 1920*1080:
        return "Photo size too big"
    return data

def get_image(post_id):
    sql = "SELECT picture FROM posts WHERE id=:post_id"
    data = db.session.execute(sql, {"post_id": post_id})
    picture = data.fetchone()[0]
    return picture