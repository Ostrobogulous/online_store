from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.get_requests import get_product_request
from OffbeatStore.utility_functions.validators import item_validation
from OffbeatStore.utility_functions.image_management import save_image
from flask import flash, render_template, redirect, url_for, g
from flask.views import MethodView
from OffbeatStore.utility_functions.operations import create_product_operation


class CreateProduct(MethodView):
    decorators = [login_required]

    @staticmethod
    def get():
        return render_template("product/create_update.html")

    @staticmethod
    def post():
        name, category, brand, description, quantity, price, image_file = get_product_request()

        error = item_validation(name, category, brand, description, quantity, price, image_file)

        if error is not None:
            flash(error)
            return render_template("product/create_update.html")
        else:
            price = float(price)
            quantity = int(quantity)

            image_location = save_image(image_file)

            create_product_operation(name, category, brand, description, quantity, price, image_location)

            return redirect(url_for("profile.profile_products", id=g.user["id"], username=g.user["username"]))
