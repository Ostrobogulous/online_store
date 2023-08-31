from flask import abort, session, request, render_template
from flask.views import View
from OffbeatStore.utility_functions.utils import remove_extra_spaces, adjust_product, sort_products, adjust_currency
from OffbeatStore.utility_functions.operations import search_products_operation


class SearchProducts(View):
    methods = ["GET"]

    def dispatch_request(self):
        keyword = request.args.get("keyword")

        if keyword is None or len(keyword) == 0:
            abort(404, f"Invalid search")

        keyword = remove_extra_spaces(keyword)

        product_rows = search_products_operation(keyword)

        products = []

        for product_row in product_rows:
            product = adjust_product(product_row)
            products.append(product)

        currency = session.get("currency", "Euro")

        for product in products:
            product["price"] = adjust_currency(product["price"], currency)

        if "sort" in request.args:
            sort_option = request.args.get("sort")
        else:
            sort_option = "latest"

        products = sort_products(sort_option, products)

        return render_template("product/search_result.html", products=products, keyword=keyword, selected_sort=sort_option)
