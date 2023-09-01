from flask import redirect, request, flash, url_for, g
from flask.views import View
from OffbeatStore.utility_functions.utils import get_product
from OffbeatStore.utility_functions.validators import review_validation
from OffbeatStore.utility_functions.decorators import  login_required
from OffbeatStore.utility_functions.get_requests import get_review_request
from OffbeatStore.utility_functions.operations import create_review_operation, user_review_exist_operation
from OffbeatStore.utility_functions.notification import add_notification, Notification


class AddReview(View):
    decorators = [login_required]

    methods = ["POST"]

    def dispatch_request(self, id):
        product = get_product(id, False)

        if user_review_exist_operation(id, g.user["id"]):
            flash("You have already made a review for this product.")
            return redirect(request.referrer or '/')

        if product["seller_id"] == g.user["id"]:
            flash("You can't make a review for your own product.")
            return redirect(request.referrer or '/')

        rating, content = get_review_request()

        error = review_validation(rating, content)

        if error is not None:
            flash(error)
            return redirect(request.referrer or '/')

        else:
            rating = int(rating)
            create_review_operation(id, rating, content)
            add_notification(product["seller_id"], id, Notification.REVIEW.value["label"])
            return redirect(url_for("product.product_page", id=id))
