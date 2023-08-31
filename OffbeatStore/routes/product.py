from OffbeatStore.views.product.create_product import CreateProduct
from OffbeatStore.views.product.update_product import UpdateProduct
from OffbeatStore.views.product.delete_product import DeleteProduct
from OffbeatStore.views.product.search_products import SearchProducts
from OffbeatStore.views.product.product_page import ProductPage
from OffbeatStore.views.product.react_product import ReactProduct
from OffbeatStore.views.product.set_currency import SetCurrency
from OffbeatStore.views.product.add_review import AddReview
from OffbeatStore.views.product.delete_review import DeleteReview
from OffbeatStore.blueprints import product_bp as bp


bp.add_url_rule("/addendum",
                view_func=CreateProduct.as_view("addendum"))

bp.add_url_rule("/update/<int:id>",
                view_func=UpdateProduct.as_view("update"))

bp.add_url_rule("/delete/<int:id>",
                view_func=DeleteProduct.as_view("delete"))

bp.add_url_rule("/search",
                view_func=SearchProducts.as_view("search"))

bp.add_url_rule("/product/<int:id>",
                view_func=ProductPage.as_view("product_page"))

bp.add_url_rule("/react/<int:id>",
                view_func=ReactProduct.as_view("react"))

bp.add_url_rule("/set_currency",
                view_func=SetCurrency.as_view("set_currency"))

bp.add_url_rule("/add_review/<int:id>",
                view_func=AddReview.as_view("add_review"))

bp.add_url_rule("/delete_review/<int:id>",
                view_func=DeleteReview.as_view("delete_review"))
