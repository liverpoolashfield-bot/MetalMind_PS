from app import create_app, db
from app.models import User, Membership, SubscriptionPlan, Subscription, Payment

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Membership': Membership,
        'SubscriptionPlan': SubscriptionPlan,
        'Subscription': Subscription,
        'Payment': Payment
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Membership.query.first():
            basic = Membership(name='Basic', description='Basic membership tier', tier=1, price=0.0, features='Basic access')
            premium = Membership(name='Premium', description='Premium membership tier', tier=2, price=19.99, features='Full access, Priority support')
            pro = Membership(name='Pro', description='Professional membership tier', tier=3, price=49.99, features='All features, Dedicated support, API access')
            db.session.add_all([basic, premium, pro])
            
            basic_plan = SubscriptionPlan(name='Basic Monthly', description='Basic plan', price=0.0, billing_cycle='monthly', membership=basic)
            premium_plan = SubscriptionPlan(name='Premium Monthly', description='Premium plan', price=19.99, billing_cycle='monthly', membership=premium)
            pro_plan = SubscriptionPlan(name='Pro Monthly', description='Pro plan', price=49.99, billing_cycle='monthly', membership=pro)
            db.session.add_all([basic_plan, premium_plan, pro_plan])
            db.session.commit()
            print('Created default memberships and plans')
    
    app.run(debug=True, host='0.0.0.0', port=5000)