from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.models import User
from app.style_transfer.models import StyleImage
from datetime import datetime


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('style_transfer.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('style_transfer.index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('style_transfer.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/profile')
@login_required
def profile():
    # Get user's style transfer statistics
    total_transfers = StyleImage.query.filter_by(user_id=current_user.id).count()

    # Get transfers from this month
    first_day_of_month = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = StyleImage.query.filter_by(user_id=current_user.id).filter(
        StyleImage.created_at >= first_day_of_month
    ).count()

    # Get recent images (limit to 6)
    recent_images = StyleImage.query.filter_by(user_id=current_user.id).order_by(
        StyleImage.created_at.desc()
    ).limit(6).all()

    # Create stats dictionary
    stats = {
        'total_transfers': total_transfers,
        'this_month': this_month,
        'favorites': 0  # Placeholder for future feature
    }

    return render_template('auth/profile.html',
                           stats=stats,
                           recent_images=recent_images)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('style_transfer.index'))