import db

def add_post(title, description, user_id, classes):
    sql = "INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

    post_id = db.last_insert_id()

    sql = "INSERT INTO item_class (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [post_id, title, value])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes


def get_classes(post_id):
    sql = "SELECT title, value FROM item_class WHERE item_id = ?"
    return db.query(sql, [post_id])

def get_posts():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    users.username,
                    users.id user_id
             FROM items, users
             WHERE items.user_id = users.id
             AND items.id = ?"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def update_post(post_id, title, description, classes):
    sql = """UPDATE items SET title = ?,
                              description = ?
                          WHERE id = ?"""
    db.execute(sql, [title, description, post_id])

    sql = "DELETE FROM item_class WHERE item_id = ?"
    db.execute(sql, [post_id])

    sql = "INSERT INTO item_class (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [post_id, title, value])

def remove_post(post_id):
    sql = "DELETE FROM item_class WHERE item_id = ?"
    db.execute(sql, [post_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [post_id])

def find_post(query):
    sql = """SELECT items.id, items.title
             FROM items
             LEFT JOIN item_class ON item_class.item_id = items.id
             WHERE items.title LIKE ? OR item_class.value LIKE ? OR items.description LIKE ?
             ORDER BY items.id DESC"""
    q = "%" + query + "%"
    return db.query(sql, [q, q, q])
