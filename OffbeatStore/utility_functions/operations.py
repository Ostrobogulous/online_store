from OffbeatStore.db import get_db
from flask import g
from werkzeug.security import generate_password_hash


def register_operation(username, password):
    db = get_db()
    try:
        query = "INSERT INTO user (username, password) VALUES (?, ?)"
        db.execute(query, (username, generate_password_hash(password)))
        db.commit()
    except db.IntegrityError:
        raise Exception(f"User {username} is already registered.")


def login_operation(username):
    query = "SELECT * FROM user WHERE username = ?"
    db = get_db()
    user = db.execute(
        query, (username,)
    ).fetchone()
    return user


def create_product_operation(name, category, brand, description, quantity, price, image_location):
    query = """INSERT INTO product(label, category, brand, description, quantity, seller_id, price, image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db = get_db()
    db.execute(query,
               (name, category, brand, description, quantity, g.user["id"], price, image_location)
               )
    db.commit()


def update_product_operation(name, category, brand, description, quantity, id, price, image_location):
    query = """UPDATE product SET label = ?, category = ?, brand = ?, description = ?, quantity = ?, updated = CURRENT_TIMESTAMP, price = ?, image = ?
               WHERE id = ?"""
    db = get_db()
    db.execute(query,
               (name, category, brand, description, quantity, price, image_location, id)
               )
    db.commit()


def delete_product_operation(id):
    db = get_db()
    query = "DELETE FROM product WHERE id = ?"
    db.execute(query, (id,))
    db.commit()
    query = "DELETE FROM reaction WHERE product_id = ?"
    db.execute(query, (id,))
    db.commit()


def search_products_operation(keyword):

    query = """SELECT p.id, label, category, brand, description, quantity, seller_id, username, published, image, price
               FROM product p JOIN user u ON p.seller_id = u.id
               WHERE lower(p.label) LIKE ? OR lower(p.category) LIKE ? OR lower(p.brand) LIKE ?"""

    db = get_db()
    product_rows = db.execute(query,
                              (f"%{keyword.lower()}%", f"%{keyword.lower()}%", f"%{keyword.lower()}%")).fetchall()
    return product_rows


def get_profile_products_operation(id):
    query = """SELECT p.id, label, category, brand, description, quantity, seller_id, username, published, image, price
               FROM product p JOIN user u ON p.seller_id = u.id
               WHERE p.seller_id = ?
               ORDER BY p.published DESC"""

    db = get_db()
    product_rows = db.execute(query, (id,)).fetchall()
    return product_rows


def count_user_products_operation(id):
    query = """SELECT COUNT(*) AS product_count
               FROM product
               WHERE seller_id = ?"""

    db = get_db()
    product_count = db.execute(query, (id,)).fetchone()[0]
    return product_count


def count_user_reviews_operation(id):
    query = """SELECT COUNT(*) AS review_count
               FROM review
               WHERE user_id = ?"""

    db = get_db()
    review_count = db.execute(query, (id,)).fetchone()[0]
    return review_count


def product_operation(id):
    query = """SELECT p.id, label, category, brand, description, quantity, seller_id, username, published, image, price
               FROM product p JOIN user u ON p.seller_id = u.id
               WHERE p.id = ?"""

    db = get_db()
    product_row = db.execute(query, (id,)).fetchone()
    return product_row


def react_operation(id, type, check, reaction_id):
    db = get_db()
    if check == type:
        query = "DELETE FROM reaction WHERE product_id = ? AND user_id = ?"
        db.execute(query,
                   (id, g.user["id"],)
                   )
    elif check is None:
        query = """INSERT INTO reaction(product_id, user_id, type)
                    VALUES (?, ?, ?)"""
        db.execute(query,
                   (id, g.user["id"], type,)
                   )
    else:
        query = """UPDATE reaction SET type = ?, updated = CURRENT_TIMESTAMP 
                WHERE id = ?"""
        db.execute(query,
                   (type, reaction_id,)
                   )
    db.commit()


def next_product_id_operation():
    query = "SELECT seq FROM SQLITE_SEQUENCE WHERE name = 'product'"
    db = get_db()
    last_id = db.execute(query).fetchone()
    if last_id is None:
        return 1
    return last_id[0] + 1


def get_product_operation(id):
    query = """SELECT p.id, label, category, brand, description, quantity, seller_id, username, image, price
               FROM product p JOIN user u ON p.seller_id = u.id
               WHERE p.id = ?"""

    db = get_db()
    product = db.execute(query, (id,)).fetchone()
    return product


def get_username_operation(user_id):
    query = "SELECT username FROM user WHERE id = ?"
    db = get_db()
    ans = db.execute(query, (user_id,)).fetchone()
    if ans:
        return ans[0]
    return None


def get_user_operation(user_id):
    query = "SELECT username, created FROM user WHERE id = ?"
    db = get_db()
    ans = db.execute(query, (user_id,)).fetchone()
    return ans


def get_reaction_operation(product_id, user_id):
    query = "SELECT type, id FROM reaction WHERE product_id = ? and user_id = ?"
    db = get_db()
    ans = db.execute(query, (product_id, user_id,)).fetchone()
    return ans


def count_reaction_operation(id):
    query = """
        SELECT
            (SELECT COUNT(*) FROM reaction WHERE product_id = ? AND type = 1),
            (SELECT COUNT(*) FROM reaction WHERE product_id = ? AND type = -1)
    """

    db = get_db()
    ans = db.execute(query, (id, id,)).fetchone()
    return ans


def user_reaction_operation(product_id, user_id):
    query = """SELECT type FROM reaction WHERE product_id = ? AND user_id = ?"""
    db = get_db()
    ans = db.execute(query, (product_id, user_id,)).fetchone()
    return ans


def load_logged_in_operation(user_id):
    query = "SELECT * FROM user WHERE id = ?"
    db = get_db()
    g.user = db.execute(
        query, (user_id,)
    ).fetchone()


def create_review_operation(product_id, rating, content):
    query = """INSERT INTO review(product_id, user_id, content, rating)
                VALUES (?, ?, ?, ?)"""
    db = get_db()
    db.execute(query,
               (product_id, g.user["id"], content, rating)
               )
    db.commit()


def get_product_reviews_operation(id):
    query = """SELECT r.id, user_id, rating, content, username
               FROM review r JOIN user u ON r.user_id = u.id
               WHERE product_id = ?"""

    db = get_db()
    reviews = db.execute(query, (id,)).fetchall()
    return reviews


def user_review_exist_operation(product_id, user_id):
    query = "SELECT id FROM review WHERE product_id = ? and user_id = ?"
    db = get_db()
    ans = db.execute(query, (product_id, user_id,)).fetchone()
    return ans


def get_reviewed_products_operation(id):
    query = """SELECT r.id as review_id, user_id, product_id AS id, rating, content, label, category, brand, description, quantity, published, image, price, seller_id, u_reviewer.username AS reviewer_username, u_seller.username AS seller_username
               FROM review r JOIN product p ON r.product_id = p.id JOIN user u_reviewer ON r.user_id = u_reviewer.id JOIN user u_seller ON p.seller_id = u_seller.id
               WHERE user_id = ?"""
    db = get_db()
    reviewed_products = db.execute(query, (id,)).fetchall()
    return reviewed_products


def get_reviewer_id_operation(id):
    query = "SELECT user_id FROM review WHERE id = ?"
    db = get_db()
    ans = db.execute(query, (id,)).fetchone()
    return ans[0]


def delete_review_operation(id):
    query = "DELETE FROM review WHERE id = ?"
    db = get_db()
    db.execute(query, (id,))
    db.commit()
