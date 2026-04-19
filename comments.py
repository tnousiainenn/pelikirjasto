import db

def get_comments(post_id):
    sql = "SELECT id, rating, comment FROM comments WHERE post_id = ? ORDER BY id DESC"
    return db.query(sql, [post_id])

def add_comment(commenter_id, post_id, rating, comment):
    sql = "INSERT INTO comments (commenter_id, post_id, rating, comment) VALUES (?, ?, ?, ?)"
    db.execute(sql, [commenter_id, post_id, rating, comment])

def average_rating(post_id):
    sql = "SELECT COALESCE(SUM(rating)/COUNT(rating),0) FROM comments WHERE post_id = ?"
    result = db.query(sql, [post_id])
    return result[0][0]
