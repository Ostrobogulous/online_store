from flask import render_template, session, request
from flask.views import View
from OffbeatStore.utility_functions.utils import adjust_product, sort_products, adjust_currency
from OffbeatStore.utility_functions.operations import get_profile_products_operation, get_username_operation


class ProfileProducts(View):

    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        username = get_username_operation(id)
        print(username)

        if "sort" in request.args:
            sort_option = request.args.get("sort")
        else:
            sort_option = "latest"

        product_rows = get_profile_products_operation(id)
        products = []

        for product_row in product_rows:

            product = adjust_product(product_row)
            products.append(product)

        currency = session.get("currency", "Euro")

        for product in products:
            product["price"] = adjust_currency(product["price"], currency)

        products = sort_products(sort_option, products)

        return render_template("profile/profile_products.html", products=products, id=id, username=username, selected_sort=sort_option)
