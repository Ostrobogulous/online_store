from flask import render_template
from flask.views import View
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.operations import get_notifications_operation, mark_as_seen_operation


class NotificationPage(View):
    decorators = [login_required]

    methods = ["GET"]

    def dispatch_request(self):
        notifications_rows = get_notifications_operation()

        notifications = []
        for notification in notifications_rows:
            notification = dict(notification)
            notifications.append(notification)
            mark_as_seen_operation(notification["id"])

        return render_template("profile/notification_page.html", notifications=notifications)
