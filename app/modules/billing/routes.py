from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Payment, Subscription, User
import stripe
from stripe import StripeError

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/')
@login_required
def index():
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.created_at.desc()).all()
    return render_template('billing/index.html', payments=payments)

@billing_bp.route('/create-checkout-session', methods=['POST', 'GET'])
@login_required
def create_checkout_session():
    plan_id = request.form.get('plan_id') or request.args.get('plan_id')
    from app.models import SubscriptionPlan
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': plan.name},
                    'unit_amount': int(plan.price * 100),
                    'recurring': {'interval': plan.billing_cycle},
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=url_for('billing.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('billing.cancel', _external=True),
            customer_email=current_user.email,
        )
        return redirect(checkout_session.url, code=303)
    except StripeError as e:
        flash(f'Payment error: {str(e)}', 'danger')
        return redirect(url_for('subscriptions.index'))

@billing_bp.route('/success')
@login_required
def success():
    return render_template('billing/success.html')

@billing_bp.route('/cancel')
@login_required
def cancel():
    flash('Payment was cancelled.', 'warning')
    return redirect(url_for('subscriptions.index'))

@billing_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_renewal_payment(invoice)
    
    return '', 200

def handle_successful_payment(session):
    email = session.get('customer_email')
    user = User.query.filter_by(email=email).first()
    if user:
        payment = Payment(
            user_id=user.id,
            stripe_payment_id=session.get('payment_intent'),
            amount=session.get('amount_total', 0) / 100,
            status='completed',
            payment_method='card'
        )
        db.session.add(payment)
        db.session.commit()

def handle_renewal_payment(invoice):
    customer_id = invoice.get('customer')
    user = User.query.filter_by(stripe_customer_id=customer_id).first()
    if user:
        payment = Payment(
            user_id=user.id,
            stripe_payment_id=invoice.get('payment_intent'),
            amount=invoice.get('amount_paid', 0) / 100,
            status='completed',
            payment_method='card'
        )
        db.session.add(payment)
        db.session.commit()

@billing_bp.route('/invoice/<int:payment_id>')
@login_required
def invoice(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('billing.index'))
    return render_template('billing/invoice.html', payment=payment)