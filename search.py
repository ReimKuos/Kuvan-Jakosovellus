from db import db

def get_groups_by_time():
    sql = "SELECT id, group_name FROM groups WHERE visible ORDER BY creation_time DESC"
    groups = db.session.execute(sql)
    return groups.fetchall()

def get_groups_by_popularity():
    sql = "SELECT G.id, G.group_name FROM groups G WHERE G.visible ORDER BY " \
          "(SELECT COUNT(P.id) FROM posts P FULL OUTER JOIN likes L ON L.post_id=P.id WHERE P.group_id=G.id AND L.active) DESC"
    groups = db.session.execute(sql)
    return groups.fetchall()

def get_groups_by_activity():
    sql = "SELECT G.id, G.group_name FROM groups G WHERE G.visible ORDER BY " \
          "(SELECT COUNT(P.id) FROM posts P WHERE P.group_id=G.id) DESC"
    groups = db.session.execute(sql)
    return groups.fetchall()


def get_groups_by_creator(creator_id: int):
    sql = "SELECT id, group_name FROM groups WHERE visible=TRUE AND creator_id=:creator_id"
    groups = db.session.execute(sql, {"creator_id": creator_id})
    return groups.fetchall()


def get_posts_in_group(group_id: int):
    sql = "SELECT id, post_title FROM posts WHERE group_id=:group_id AND visible"
    results = db.session.execute(sql, {"group_id": group_id})
    return results.fetchall()

