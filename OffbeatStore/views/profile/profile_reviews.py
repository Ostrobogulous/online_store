from flask import render_template
from flask.views import View
from OffbeatStore.utility_functions.operations import get_reviewed_products_operation, get_username_operation
from OffbeatStore.utility_functions.utils import adjust_product


class ProfileReviews(View):

    methods = ["GET"]

    def dispatch_request(self, id):
        username = get_username_operation(id)

        reviewed_products_rows = get_reviewed_products_operation(id)

        reviewed_products = []

        for product_row in reviewed_products_rows:
            product = adjust_product(product_row)
            reviewed_products.append(product)

        reviewed_products = reversed(reviewed_products)

        return render_template("profile/profile_reviews.html", reviewed_products=reviewed_products, id=id, username=username)
