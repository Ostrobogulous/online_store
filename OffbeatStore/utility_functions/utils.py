from flask import g
from werkzeug.exceptions import abort
from datetime import datetime
from OffbeatStore.utility_functions.operations import get_product_operation, get_username_operation, get_user_operation, get_reaction_operation, \
    count_reaction_operation, user_reaction_operation
from OffbeatStore.services.currency_converter import ExchangeRateClient
from os import environ


def remove_extra_spaces(string):
    begin = 0; end = len(string)
    for i in range(len(string)):
        if string[i] != ' ':
            begin = i
            break
    for i in range(len(string) - 1, -1, -1):
        if string[i] != ' ':
            end = i
            break
    string = string[begin : end+1]
    keyword = ""
    for i in range(len(string)):
        if string[i] == " " and string[i - 1] == " ":
            continue
        else:
            keyword += string[i]

    return keyword
 

def get_product(id, check_seller=True):  # check seller is true when we want to update or delete a product
    product = get_product_operation(id)

    if product is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_seller and product["seller_id"] != g.user["id"]:
        abort(403)

    return product


def get_username_by_id(user_id):
    ans = get_username_operation(user_id)
    if ans:
        return ans[0]
    else:
        abort(404, f"Profile id {user_id} doesn't exist.")


def get_user_by_id(user_id):
    ans = get_user_operation(user_id)
    if ans:
        return ans[0], ans[1]
    else:
        abort(404, f"Profile id {user_id} doesn't exist.")


def reacted(product_id, user_id):
    ans = get_reaction_operation(product_id, user_id)
    if ans:
        return ans[0], ans[1]
    else:
        return None, None


def count_reaction(id):
    ans = count_reaction_operation(id)
    likes = ans[0]
    dislikes = ans[1]
    if likes is None:
        likes = 0
    if dislikes is None:
        dislikes = 0

    return likes, dislikes


def check_user_reaction(product_id, user_id):
    ans = user_reaction_operation(product_id, user_id)
    if ans:
        return ans[0]
    else:
        return 0


def get_reaction_settings(user_interaction):
    like_icon = "fa fa-thumbs-o-up fa-lg"
    like_color = "black"
    dislike_icon = "fa fa-thumbs-o-down fa-lg"
    dislike_color = "black"
    if user_interaction == 1:
        like_icon = "fa fa-thumbs-up fa-lg"
        like_color = "blue"
    elif user_interaction == -1:
        dislike_icon = "fa fa-thumbs-down fa-lg"
        dislike_color = "red"

    return like_icon, dislike_icon, like_color, dislike_color


def adjust_product(product_row):
    product = dict(product_row)
    likes, dislikes = count_reaction(product["id"])
    if g.user is None:
        user_reaction = 0
    else:
        user_reaction = check_user_reaction(product["id"], g.user["id"])
    product["event_time"] = datetime.strptime(str(product["published"]), "%Y-%m-%d %H:%M:%S")
    product["likes"] = likes
    product["dislikes"] = dislikes
    product["reactions"] = product["likes"] + product["dislikes"]
    like_icon, dislike_icon, like_color, dislike_color = get_reaction_settings(user_reaction)
    product["reaction_settings"] = {"like_icon": like_icon, "dislike_icon": dislike_icon, "like_color": like_color,
                                    "dislike_color": dislike_color}

    return product


def adjust_currency(price, currency):
    if currency != "EUR":
        currency_converter_api_key = environ["CURRENCY_CONVERTER_API_KEY"]
        exchange_client = ExchangeRateClient(currency_converter_api_key)
        price = float(format(exchange_client.convert_price(price, currency), ".2f"))

    return price


def sort_products(option, products):
    if option == "likes-count":
        products = sorted(products, key=lambda el: el["likes"], reverse=True)
    elif option == "dislikes-count":
        products = sorted(products, key=lambda el: el["dislikes"], reverse=True)
    elif option == "reactions-count":
        products = sorted(products, key=lambda el: el["reactions"], reverse=True)
    elif option == "price-ascending":
        products = sorted(products, key=lambda el: el["price"], reverse=False)
    elif option == "price-descending":
        products = sorted(products, key=lambda el: el["price"], reverse=True)
    else:
        ok = True
        if option == "oldest":
            ok = False
        products = sorted(products, key=lambda el: el["event_time"], reverse=ok)

    return products
