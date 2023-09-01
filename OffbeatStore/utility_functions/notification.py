from flask import g
from OffbeatStore.utility_functions.operations import add_notification_operation
from enum import Enum


def add_notification(user_id, product_id, notification_type):
    if g.user["id"] != user_id:

        add_notification_operation(user_id, product_id, notification_type)


class Notification(Enum):
    REVIEW = {"label": "review", "message": "reviewed your product"}
    LIKE = {"label": "like", "message": "liked your product"}
    DISLIKE = {"label": "dislike", "message": "disliked your product"}


def get_notification_message(notification_type):
    for notification in Notification:
        if notification.value["label"] == notification_type:
            return notification.value["message"]
    return "did something to your product"
