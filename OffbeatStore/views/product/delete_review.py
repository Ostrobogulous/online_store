from flask.views import View
from flask import url_for, redirect, g
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.operations import delete_review_operation, get_reviewer_id_operation


class DeleteReview(View):
    decorators = [login_required]

    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        reviewer_id = get_reviewer_id_operation(id)

        if reviewer_id == g.user["id"]:
            delete_review_operation(id)
            return redirect(url_for("profile.profile_reviews", id=g.user["id"], username=g.user["username"]))
        else:
            return redirect(url_for("main.index"))
