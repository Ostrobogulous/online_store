from flask import redirect, request, g
from flask.views import View
from OffbeatStore.utility_functions.utils import reacted, get_product
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.operations import react_operation


class ReactProduct(View):
    decorators = [login_required]

    methods = ["GET", "POST"]

    def dispatch_request(self, id):
        get_product(id, False)

        reaction_type = int(request.args.get("type"))

        check, reaction_id = reacted(id, g.user["id"])

        react_operation(id, reaction_type, check, reaction_id)

        return redirect(request.referrer or '/')
