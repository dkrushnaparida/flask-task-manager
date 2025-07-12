from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import RegisterForm, LoginForm, TaskForm
from app.models import User, Task
from app import db
from flask import abort
from app.utils import get_location, get_weather
import requests
from datetime import date
from flask import jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

def get_jokes():
    try:
        res = requests.get("https://official-joke-api.appspot.com/jokes/ten")
        if res.status_code == 200:
            return res.json()[:3]
    except Exception as e:
        print("Joke error:", e)
    return []

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
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    lat, lon, city = get_location()
    weather = get_weather(lat, lon)
    return render_template("dashboard.html", tasks=tasks, weather=weather, city=city)

@main.route("/api/jokes")
@login_required
def fetch_jokes():
    jokes = get_jokes()[:3]  # Limit to 3 jokes
    return jsonify(jokes)


@main.route("/task/new", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data,
            owner=current_user
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("create_task.html", form=form, legend="New Task", today=date.today().isoformat())


@main.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        abort(403)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("create_task.html", form=form, legend="Edit Task")

@main.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "info")
    return redirect(url_for("main.dashboard"))
