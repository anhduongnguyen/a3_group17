from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        email_input = login_form.email.data
        password = login_form.password.data

        user = db.session.scalar(db.select(User).where(User.email == email_input))

        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password, password):  # match against hashed password
            error = 'Incorrect password'

        if error is None:
            login_user(user)
            flash('You logged in successfully.', 'success')

            nextp = request.args.get('next')
            if not nextp or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error, 'danger')

    return render_template('login.html', form=login_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        existing_user = db.session.scalar(db.select(User).where(User.email == register_form.email.data))
        if existing_user:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for('auth.register'))
        else:
            new_user = User(
                first_name=register_form.first_name.data,
                surname=register_form.surname.data,
                email=register_form.email.data,
                contact_number=register_form.contact_number.data,
                address=register_form.street_address.data,
                password=generate_password_hash(register_form.password.data)
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash("Registration successful. You are now logged in.", "success")
            return redirect(url_for('main.index'))

    return render_template('register.html', form=register_form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))
