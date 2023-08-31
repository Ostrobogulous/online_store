from flask import render_template, session, flash, redirect, url_for, request, g
from flask.views import MethodView
from werkzeug.security import check_password_hash
from OffbeatStore.utility_functions.operations import login_operation, load_logged_in_operation
from OffbeatStore.utility_functions.decorators import logged_in
from OffbeatStore.blueprints import authentication_bp as bp


class Login(MethodView):
    decorators = [logged_in]

    @staticmethod
    def login_validation(user, password):
        if user is None:
            return "Incorrect username."

        if not check_password_hash(user["password"], password):
            return "Incorrect password."

        return None

    @staticmethod
    def get():
        return render_template("authentication/login.html")

    @staticmethod
    def post():
        username = request.form["username"]
        password = request.form["password"]

        user = login_operation(username)

        error = Login.login_validation(user, password)

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("main.index"))

        flash(error)
        return render_template("authentication/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        load_logged_in_operation(user_id)
