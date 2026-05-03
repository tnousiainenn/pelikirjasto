import db

def get_comments(post_id):
    sql = "SELECT id, rating, comment FROM comments WHERE post_id = ? ORDER BY id DESC"
    return db.query(sql, [post_id])



def get_comment(comment_id):
    sql = "SELECT id, rating, comment, commenter_id FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])


def add_comment(commenter_id, post_id, rating, comment):
    sql = "INSERT INTO comments (commenter_id, post_id, rating, comment) VALUES (?, ?, ?, ?)"
    db.execute(sql, [commenter_id, post_id, rating, comment])

def average_rating(post_id):
    sql = "SELECT COALESCE(SUM(rating)/COUNT(rating),0) FROM comments WHERE post_id = ?"
    result = db.query(sql, [post_id])
    return result[0][0]
