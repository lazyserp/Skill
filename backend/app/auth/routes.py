from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .forms import RegisterForm, LoginForm
from app.models.user import User
from app.extensions import db, login_manager
from app.auth import auth_bp



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already registered', 'danger')
            return redirect(url_for('auth.register'))
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful', 'success')
        return redirect(url_for('auth.login'))
    return render_template("register.html.j2", form=form)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully!', 'success')
            return redirect(url_for('auth.login'))  # placeholder redirect
        flash('Invalid username or password', 'danger')
    return render_template('login.html.j2', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
