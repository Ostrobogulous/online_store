from flask import render_template, session
from flask.views import View
from OffbeatStore.utility_functions.utils import get_product, adjust_product, adjust_currency
from OffbeatStore.utility_functions.operations import product_operation, get_product_reviews_operation


class ProductPage(View):
    methods = ["GET"]

    def dispatch_request(self, id):
        get_product(id, False)

        product_row = product_operation(id)

        currency = session.get("currency", "Euro")

        product = adjust_product(product_row)

        reviews = get_product_reviews_operation(id)

        product["price"] = adjust_currency(product["price"], currency)

        return render_template("product/product_page.html", product=product, reviews=reviews)
