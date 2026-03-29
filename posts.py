import db

def add_post(title, genre, description, user_id):
    sql = "INSERT INTO items (title, genre, description, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, genre, description, user_id])

def get_posts():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT items.id,
                    items.title,
                    items.genre,
                    items.description,
                    users.username,
                    users.id user_id
             FROM items, users
             WHERE items.user_id = users.id
             AND items.id = ?"""
    return db.query(sql, [post_id])[0]

def update_post(post_id, title, genre, description):
    sql = """UPDATE items SET title = ?,
                              genre = ?,
                              description = ?
                          WHERE id = ?"""
    db.execute(sql, [title, genre, description, post_id])

def remove_post(post_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [post_id])

def find_post(query):
    sql = """SELECT id, title
             FROM items
             WHERE title LIKE ? OR genre LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    q = "%" + query + "%"
    return db.query(sql, [q, q, q])
