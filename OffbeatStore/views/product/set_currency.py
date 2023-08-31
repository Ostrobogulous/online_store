from flask import session, request, redirect
from flask.views import View


class SetCurrency(View):
    methods = ["POST"]

    def dispatch_request(self):
        selected_currency = request.form["currency"]
        session["currency"] = selected_currency
        return redirect(request.referrer or '/')
