from flask import redirect, url_for, g
from flask.views import View
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.utils import get_product
from OffbeatStore.utility_functions.image_management import delete_image
from OffbeatStore.utility_functions.operations import delete_product_operation


class DeleteProduct(View):
    decorators = [login_required]

    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        product = get_product(id)

        delete_image(product["image"])

        delete_product_operation(id)

        return redirect(url_for("profile.profile_products", id=g.user["id"], username=g.user["username"]))
