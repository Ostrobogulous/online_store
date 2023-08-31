from OffbeatStore.utility_functions.operations import add_notification_operation


def add_notification(user_id, product_id, notification_type):
    match notification_type:
        case "like":
            notification_message = "liked your product"
        case "dislike":
            notification_message = "disliked your product"
        case "review":
            notification_message = "reviewed your product"
        case _:
            notification_message = "did something"

    add_notification_operation(user_id, product_id, notification_message, notification_type)

