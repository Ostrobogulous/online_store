from OffbeatStore.views.profile.profile_page import ProfilePage
from OffbeatStore.views.profile.profile_products import ProfileProducts
from OffbeatStore.views.profile.profile_reviews import ProfileReviews
from OffbeatStore.blueprints import profile_bp as bp


bp.add_url_rule("/profile/<int:id>",
                view_func=ProfilePage.as_view("profile_page"))

bp.add_url_rule("/profile/<int:id>/products",
                view_func=ProfileProducts.as_view("profile_products"))

bp.add_url_rule("/profile/<int:id>/reviews",
                view_func=ProfileReviews.as_view("profile_reviews"))
