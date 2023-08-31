from OffbeatStore.views.authentication.logout import Logout
from OffbeatStore.views.authentication.login import Login
from OffbeatStore.views.authentication.register import Register
from OffbeatStore.blueprints import authentication_bp as bp


bp.add_url_rule("/logout/",
                view_func=Logout.as_view("logout"))

bp.add_url_rule("/login/",
                view_func=Login.as_view("login"))

bp.add_url_rule("/register/",
                view_func=Register.as_view("register"))
