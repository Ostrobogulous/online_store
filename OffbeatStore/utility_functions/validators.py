def review_validation(rating, content):
    if not rating.isdigit():
        return "Rating must be an integer."

    if not 1 <= int(rating) <= 5:
        return "Rating must be between 1 and 5."
    return None


def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def item_validation(name, category, brand, description, quantity, price, image_file):
    if not quantity.isdigit():
        return "Quantity must be an integer."

    try:
        float(price)
    except ValueError:
        return "Price must be a number."

    if round(float(price), 2) != float(price):
        return "Price must corresponds to fractions of cents."

    if len(name) > 60:
        return "Name length limit exceeded."

    if len(category) > 60:
        return "Category length limit exceeded."

    if len(brand) > 60:
        return "Brand length limit exceeded."

    if len(description) > 1100:
        return "Description length limit exceeded."

    if int(quantity) <= 0:
        return "Quantity can't be negative or null."
    if float(price) < 0:
        return "Invalid price."

    if image_file is not None and image_file.filename != '' and not allowed_file(image_file.filename):
        return "Invalid image type. Allowed image types are jpg, jpeg and png."

    return None
