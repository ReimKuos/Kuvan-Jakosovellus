from db import db
from flask import make_response


def get_groups_by_time():
    sql = "SELECT id, group_name FROM groups WHERE visible=TRUE AND public=TRUE ORDER BY creation_time"
    groups = db.session.execute(sql)
    return groups.fetchall()


def get_groups_by_creator(creator_id: int):
    sql = "SELECT group_name FROM groups WHERE visible=TRUE AND creator_id=:creator_id"
    groups = db.session.execute(sql, {"creator_id": creator_id})
    return [group[0] for group in groups.fetchall()]


def get_groups_by_membership(member_id: int):
    sql = "SELECT group_name FROM groups WHERE visible=TRUE AND group id IN" \
          "(SELECT group_id FROM members WHERE member_id=:member_id)"
    groups = db.session.execute(sql, {"member_id": member_id})
    return [group[0] for group in groups.fetchall()]


def get_adminastrated_groups(adm_id: int):
    sql = "SELECT group_name FROM groups WHERE visible=TRUE AND group id IN" \
          "(SELECT group_id FROM adminastrators WHERE adminastrator_id=:adm_id)"
    groups = db.session.execute(sql, {"adm_id": adm_id})
    return [group[0] for group in groups.fetchall()]


def get_posts_in_group(group_id: int):
    sql = "SELECT id, post_title FROM posts WHERE group_id=:group_id AND visible"
    results = db.session.execute(sql, {"group_id": group_id})
    return results