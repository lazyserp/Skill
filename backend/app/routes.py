from flask import Flask, render_template, redirect, url_for, flash, request,session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.forms import RegisterForm, LoginForm
import os
from app.forms import EditProfileForm


app = Flask(__name__)
app.config.from_object('app.config.Config')


# Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html.j2')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html.j2', user=current_user)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already registered', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful', 'success')
        return redirect(url_for('login'))
    return render_template("register.html.j2", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully!', 'success')

            session['user_id'] = user.id
            from datetime import timedelta
            app.permanent_session_lifetime = timedelta(days=1)
            session.permanent = True

            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.skills_to_teach = form.skills_to_teach.data
        current_user.skills_to_learn = form.skills_to_learn.data
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("dashboard"))

    # Pre-fill form fields
    if request.method == "GET":
        form.bio.data = current_user.bio
        form.skills_to_teach.data = current_user.skills_to_teach
        form.skills_to_learn.data = current_user.skills_to_learn

    return render_template("edit_profile.html.j2", form=form)

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    search_query = request.args.get('search', '')
    if search_query:
        users = User.query.filter(
            (User.username.contains(search_query)) | (User.email.contains(search_query))
        ).all()
    else:
        users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/promote/<int:user_id>', methods=['POST'])
def promote_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/demote/<int:user_id>', methods=['POST'])
def demote_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = False
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


# @app.route('/make-admin')
# def make_admin():
#     username = request.args.get('username')
#     if not username:
#         return "❌ Please provide username like ?username=yourname"

#     user = User.query.filter_by(username=username).first()
#     if user:
#         user.is_admin = True
#         db.session.commit()
#         return f"✅ {username} is now an admin!"
#     return "❌ User not found"