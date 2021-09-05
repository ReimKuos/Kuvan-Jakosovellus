from db import db

def add_comment(commenter_id, commented_id, comment):
    sql = "INSERT INTO comments (visible, commenter_id, commented_id, comment)" \
          "VALUES (TRUE, :commenter_id, :commented_id, :comment)"
    try:
        db.session.execute(sql, {
            "commenter_id": commenter_id,
            "commented_id": commented_id,
            "comment": comment
        })
        db.session.commit()
        return True
    except:
        return False

def get_comments(post_id):
    sql = "SELECT C.id, C.commenter_id, C.comment, U.name FROM comments C LEFT JOIN users U " \
          "ON C.commenter_id = U.id WHERE C.commented_id=:post_id"
    comments = db.session.execute(sql, {"post_id": post_id})
    return comments.fetchall()