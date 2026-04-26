from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Membership
from app.modules.members.forms import ProfileForm

members_bp = Blueprint('members', __name__)

@members_bp.route('/')
@members_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('members/dashboard.html', user=current_user)

@members_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('members.profile'))
    return render_template('members/profile.html', form=form)

@members_bp.route('/membership')
@login_required
def membership():
    memberships = Membership.query.filter_by(is_active=True).all()
    return render_template('members/membership.html', memberships=memberships)

@members_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('members/settings.html')