from flask import redirect, url_for
from OffbeatStore.views.main.index import Index
from OffbeatStore.blueprints import main_bp as bp


@bp.route("/", methods=["GET", "POST"])
def root():
    return redirect(url_for("main.index"))


bp.add_url_rule("/home",
                view_func=Index.as_view("index"))
