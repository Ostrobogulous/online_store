from flask import redirect, request, g
from flask.views import View
from OffbeatStore.utility_functions.utils import reacted, get_product
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.operations import react_operation
from OffbeatStore.utility_functions.notification import add_notification, Notification


class ReactProduct(View):
    decorators = [login_required]

    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        product = get_product(id, False)

        reaction_type = int(request.args.get("type"))

        check, reaction_id = reacted(id, g.user["id"])

        react_operation(id, reaction_type, check, reaction_id)

        if check != reaction_type:
            notification_type = Notification.DISLIKE.value["label"]
            if reaction_type == 1:
                notification_type = Notification.LIKE.value["label"]

            add_notification(product["seller_id"], g.user["id"], id, notification_type)

        return redirect(request.referrer or '/')
