from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Login failed', 'danger')

    return render_template('login.html')


@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))