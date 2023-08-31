from flask import session, redirect, url_for
from flask.views import View


class Logout(View):
    def dispatch_request(self):
        session.clear()
        return redirect(url_for("main.index"))
