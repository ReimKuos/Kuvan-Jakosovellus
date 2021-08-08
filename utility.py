from db import db

def get_user_id(user_id: str):
    sql = "SELECT id FROM users WHERE user_id=:user_id"
    id = db.session.execute(sql, {"user_id": user_id})
    return id.fetchone()[0]

def get_group_info(group_id: int):
    sql = "SELECT group_name, description, num_posts FROM groups WHERE id=:group_id"
    name = db.session.execute(sql, {"group_id": group_id})
    return name.fetchone()[0]