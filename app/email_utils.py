from flask_mail import Message
from app import mail

def send_limit_warning_email(user_email, category, total_spent, limit):
    msg = Message(
        subject=f"Budget Alert: {category}",
        recipients=[user_email],
        body=(
            f"Hello!\n\n"
            f"You have exceeded your budget for category '{category}'.\n"
            f"Limit: {limit} €\n"
            f"Spent: {total_spent} €\n\n"
            f"Please review your expenses.\n"
        )
    )
    mail.send(msg)
