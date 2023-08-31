from flask import render_template
from flask.views import View
from OffbeatStore.utility_functions.utils import get_user_by_id
from OffbeatStore.utility_functions.operations import count_user_products_operation, count_user_reviews_operation


class ProfilePage(View):

    methods = ["GET"]

    def dispatch_request(self, id):
        username, created = get_user_by_id(id)
        product_count = count_user_products_operation(id)
        review_count = count_user_reviews_operation(id)
        user = dict()
        user["username"] = username
        user["created"] = created
        user["product_count"] = product_count
        user["review_count"] = review_count

        return render_template("profile/profile_page.html", id=id, user=user)
