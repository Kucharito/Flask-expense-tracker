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

def notify_user(user_id, message, type='info', notificiation=None):
    #flash(message, type)
    exists = Notification.query.filter_by(user_id=user_id, message=message).first()
    if exists:
        return

    create_notification(user_id, message, type)
    db.session.add(notificiation)
    db.session.commit()
