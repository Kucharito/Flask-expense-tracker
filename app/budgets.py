from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.email_utils import send_limit_warning_email
from app.notifications_utils import create_notification, notify_user

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@budgets_bp.route('/', methods=['GET', 'POST'])
@login_required
def list_budgets():
    from app import db
    from app.models import Budget
    from sqlalchemy import func
    from app.forms import BudgetForm
    from app.models import Expense

    form = BudgetForm()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        new_budget = Budget(
            category=form.category.data,
            limit=form.limit.data,
            user_id=current_user.id
        )
        db.session.add(new_budget)
        db.session.commit()
        notify_user(current_user.id,f'New budget set for {form.category.data} with limit {form.limit.data}.','info')
        return redirect(url_for('budgets.list_budgets'))

    budgets_data = []
    for b in budgets:
        total_spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            Expense.category == b.category
        ).scalar() or 0

        limit = float(b.limit) if b.limit is not None else 0
        remaining = float(b.limit) - total_spent
        percent_used = (total_spent / b.limit * 100) if b.limit > 0 else 0

        if percent_used >= 100 and not b.notified_over_limit:
            if not b.last_email_sent or (datetime.utcnow() - b.last_email_sent) > timedelta(minutes=10):
                send_limit_warning_email(
                    user_email=current_user.email,
                    category=b.category,
                    total_spent=total_spent,
                    limit=b.limit
                )
                b.last_email_sent = datetime.utcnow()
                db.session.commit()

            notify_user(current_user.id, f'You have exceeded your budget for {b.category}!', 'warning')
            b.notified_over_limit = True
            db.session.commit()


        elif limit > 0 and percent_used >= 80:
            status = 'warning'
            b.notified_near_limit = True
            notify_user(current_user.id, f'You are nearing your budget limit for {b.category}.', 'warning')
        elif percent_used < 80:
            b.notified_near_limit = False
            b.notified_over_limit = False
            db.session.commit()
        else:
            status = 'ok'


        total_budget = sum(b.limit for b in budgets)
        total_expenses = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id
        ).scalar() or 0

        remaining_overall = total_budget - total_expenses if total_budget > 0 else 0


        budgets_data.append({
            'category': b.category,
            'limit': b.limit,
            'total_spent': total_spent,
            'remaining': remaining,
            'percent_used': percent_used
        })

    return render_template('budgets_dashboard.html', budgets=budgets_data, form=form, total_budget=total_budget, total_spent=total_expenses, remaining_overall=remaining_overall)

@budgets_bp.route('/test-email')
@login_required
def test_email():
    from app.email_utils import send_limit_warning_email
    send_limit_warning_email(
        user_email=current_user.email,
        category='Test Category',
        total_spent=150,
        limit=100
    )
    flash('Test email sent!', 'info')
    return redirect(url_for('budgets.list_budgets'))