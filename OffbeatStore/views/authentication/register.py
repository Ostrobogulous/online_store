from flask import render_template, flash, url_for, redirect, request
from flask.views import MethodView
from OffbeatStore.utility_functions.operations import register_operation
from OffbeatStore.utility_functions.decorators import logged_in


class Register(MethodView):
    decorators = [logged_in]

    @staticmethod
    def register_validation(username, password, password_confirmation):
        if len(username) < 3 or len(username) > 20:
            return "Username length must be between 3 and 20 characters."

        if password != password_confirmation:
            return "Invalid password."

        if len(password) < 8:
            return "Password must contain at least 8 characters."

        if password.find(username) != -1:
            return "Password shouldn't contain your username"

        return None

    @staticmethod
    def get():
        return render_template("authentication/register.html")

    @staticmethod
    def post():
        username = request.form["username"]
        password = request.form["password"]
        password_confirmation = request.form["password_confirmation"]

        error = Register.register_validation(username, password, password_confirmation)

        if error is None:
            try:
                register_operation(username, password)
            except Exception as e:
                error = str(e)
            else:
                return redirect(url_for("authentication.login"))

        flash(error)
        return render_template("authentication/register.html", error=error)
