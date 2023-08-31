from flask import flash, render_template, redirect, url_for, g
from flask.views import MethodView
from OffbeatStore.utility_functions.utils import get_product
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.get_requests import get_product_request
from OffbeatStore.utility_functions.validators import item_validation
from OffbeatStore.utility_functions.image_management import save_image
from OffbeatStore.utility_functions.operations import update_product_operation


class UpdateProduct(MethodView):
    decorators = [login_required]

    @staticmethod
    def get(id):
        product = get_product(id)
        return render_template("product/create_update.html", product=product)

    @staticmethod
    def post(id):
        product = get_product(id)

        name, category, brand, description, quantity, price, image_file = get_product_request()

        error = item_validation(name, category, brand, description, quantity, price, image_file)

        if error is not None:
            flash(error)
            return render_template("product/create_update.html", product=product)
        else:
            image_location = save_image(image_file, product["image"], id)

            update_product_operation(name, category, brand, description, quantity, id, price, image_location)

            return redirect(url_for("profile.profile_products", id=g.user["id"], username=g.user["username"]))
