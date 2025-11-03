from flask import flash

from app import db
from app.models import Notification


def create_notification(user_id, message, type='info'):

    notification = Notification(
        user_id=user_id,
        message=message,
        type=type
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def notify_user(user_id, message, type='info'):
    from flask import flash
    from app.models import Notification
    from app import db

    #flash(message, type)
    notification = Notification(
        user_id=user_id,
        message=message,
        type=type
    )
    db.session.add(notification)
    db.session.commit()

