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