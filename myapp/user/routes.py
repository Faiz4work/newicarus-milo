from flask import Blueprint, redirect, url_for, request, flash, render_template
from myapp.user.forms import LoginForm
from myapp.models import Users
from flask_login import login_user, logout_user, current_user

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        remember = request.form.get('remember')

        user = Users.query.filter_by(email=email).first()
        if user:
            if user.email == email and user.password == password:
                login_user(user, remember=remember)
                return redirect(url_for('main.home'))
            else:
                flash('Username or password incorrect!', 'info')
                return redirect(url_for('user.login'))
        else:
            flash('No user exist with this email address', 'danger')
            return redirect(url_for('user.login'))
    return render_template('user/login.html', form=form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.home"))