import functools
from flask import redirect, url_for, g


def logged_in(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            return redirect(url_for("main.index"))
        return view(**kwargs)

    return wrapped_view


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("authentication.login"))
        return view(**kwargs)

    return wrapped_view
