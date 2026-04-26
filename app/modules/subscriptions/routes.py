from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import SubscriptionPlan, Subscription

subscriptions_bp = Blueprint('subscriptions', __name__)

@subscriptions_bp.route('/')
@login_required
def index():
    plans = SubscriptionPlan.query.filter_by(is_active=True).all()
    current_sub = Subscription.query.filter_by(user_id=current_user.id, status='active').first()
    return render_template('subscriptions/index.html', plans=plans, current_sub=current_sub)

@subscriptions_bp.route('/subscribe/<int:plan_id>', methods=['POST'])
@login_required
def subscribe(plan_id):
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    return redirect(url_for('billing.create_checkout_session', plan_id=plan_id))

@subscriptions_bp.route('/cancel/<int:subscription_id>', methods=['POST'])
@login_required
def cancel(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    if subscription.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('subscriptions.index'))
    
    subscription.status = 'cancelled'
    subscription.auto_renew = False
    db.session.commit()
    flash('Subscription cancelled. You will retain access until end of billing period.', 'info')
    return redirect(url_for('subscriptions.index'))

@subscriptions_bp.route('/change/<int:plan_id>', methods=['POST'])
@login_required
def change_plan(plan_id):
    new_plan = SubscriptionPlan.query.get_or_404(plan_id)
    current_sub = Subscription.query.filter_by(user_id=current_user.id, status='active').first()
    
    if current_sub:
        current_sub.plan_id = new_plan.id
        db.session.commit()
        flash(f'Plan changed to {new_plan.name}', 'success')
    
    return redirect(url_for('subscriptions.index'))