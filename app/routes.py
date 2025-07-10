from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import RegisterForm, LoginForm
from app.models import User
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account Created", 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('invalidate username and password', 'danger')

    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout', 'info')
    return redirect(url_for('main.login'))

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")