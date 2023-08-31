from flask import request


def get_product_request():
    name = request.form["name"]
    category = request.form["category"]
    brand = request.form["brand"]
    description = request.form["description"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    if 'image' in request.files:
        image_file = request.files['image']
    else:
        image_file = None

    return name, category, brand, description, quantity, price, image_file


def get_review_request():
    rating = request.form["rating"]
    content = request.form["content"]

    return rating, content
