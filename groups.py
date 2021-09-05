from db import db

def check_group_existance(group_name: str):
    sql = "SELECT id FROM groups WHERE group_name=:group_name"
    check = db.session.execute(sql, {"group_name": group_name})
    check = check.fetchall()
    if check is not None:
        return True
    return False 


def create_group(creator_id: int, group_name: str, description: str):
    sql = "INSERT INTO groups (creator_id, creation_time, visible, group_name, description)" \
          "VALUES (:creator_id, NOW(), TRUE, :group_name, :description)"
    try:
        db.session.execute(sql, {
            "creator_id": creator_id,
            "group_name": group_name,
            "description": description
        })
        db.session.commit()
        return True
    except:
        return False


def delete_group(group_id: int):
    try:
        sql = "UPDATE groups SET visible=FALSE WHERE id=:group_id"
        db.session.execute(sql, {"group_id": group_id})
        return True
    except:
        return False


def toggle_group_public_status(group_id: int, status: bool):
    try:
        sql = "UPDATE groups SET public=:status WHERE id=:group_id"
        db.session.execute(sql, {"group_id": group_id, "public": status})
        db.session.commit()
        return True
    except:
        return False
    

def check_group_priviledges(group_id: int, user_id: int):
    sql = "SELECT adminastrator_id FROM adminastrators WHERE group_id=:group_id"
    adminastrators = db.session.execute(sql, {"group_id": group_id})
    if user_id in adminastrators.fetchall():
        return True
    return False


def give_group_priviledges(group_id: int, user_id: int):
    try:
        sql = "INSERT INTO adminastrators (group_id, adminastrator_id) " \
              "VALUES (:group_id, :user_id)"
        db.session.execute(sql, {"group_id": group_id, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False
