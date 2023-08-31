from flask import render_template
from flask.views import View
from OffbeatStore.utility_functions.decorators import login_required
from OffbeatStore.utility_functions.operations import get_notifications_operation, mark_as_seen_operation
from datetime import datetime, timedelta


class NotificationPage(View):
    decorators = [login_required]

    methods = ["GET"]

    @staticmethod
    def format_notification_date(created):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        if created.date() == today:
            return f"Today | {created.strftime('%H:%M')}"
        elif created.date() == yesterday:
            return f"Yesterday | {created.strftime('%H:%M')}"
        else:
            return created.strftime('%d-%m-%Y | %H:%M')

    def dispatch_request(self):
        notifications_rows = get_notifications_operation()

        notifications = []
        for notification in notifications_rows:
            notification = dict(notification)
            notification["created"] = self.format_notification_date(notification["created"])
            notifications.append(notification)
            mark_as_seen_operation(notification["id"])

        return render_template("profile/notification_page.html", notifications=notifications)
