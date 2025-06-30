from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import timedelta
from app.extensions import db
from app.models.user import User
from app.forms import RegisterForm, LoginForm, EditProfileForm

auth_bp = Blueprint("auth", __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You don't have permission.", "danger")
            return redirect(url_for('auth.dashboard'))
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/')
def home():
    return render_template("landing.html.j2")

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html.j2', user=current_user)

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('auth.login'))
    return render_template("register.html.j2", form=form)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            session.permanent = True
            return redirect(url_for('auth.dashboard'))

        flash('Invalid credentials', 'danger')
    return render_template('login.html.j2', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.skills_to_teach = form.skills_to_teach.data
        current_user.skills_to_learn = form.skills_to_learn.data
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("auth.dashboard"))

    if request.method == "GET":
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        form.skills_to_teach.data = current_user.skills_to_teach
        form.skills_to_learn.data = current_user.skills_to_learn

    return render_template("edit_profile.html.j2", form=form)

@auth_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    search_query = request.args.get('search', '')
    if search_query:
        users = User.query.filter(
            (User.username.contains(search_query)) | (User.email.contains(search_query))
        ).all()
    else:
        users = User.query.all()
    return render_template('admin_dashboard.html.j2', users=users)

@auth_bp.route('/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        user.is_admin = True
        db.session.commit()
    return redirect(url_for('auth.admin_dashboard'))

@auth_bp.route('/demote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def demote_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        user.is_admin = False
        db.session.commit()
    return redirect(url_for('auth.admin_dashboard'))

@auth_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('auth.admin_dashboard'))

@auth_bp.route('/make-admin')
@login_required
@admin_required
def make_admin():
    username = request.args.get('username')
    if not username:
        return "❌ Please provide username like ?username=yourname"

    user = User.query.filter_by(username=username).first()
    if user:
        user.is_admin = True
        db.session.commit()
        return f"✅ {username} is now an admin!"
    return "❌ User not found"
