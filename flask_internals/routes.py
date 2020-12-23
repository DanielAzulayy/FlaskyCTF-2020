from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, abort, session, send_from_directory, render_template_string)
from .forms import LoginForm, GetEmailForm, SignupForm
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import db, User

# Blueprint Configuration
main_bp = Blueprint('main_bp',
                    __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/')
def main():
    return render_template('index.html')

@main_bp.route('/robots.txt')
def load_robots_txt():
    return main_bp.send_static_file('robots.txt')

@main_bp.route('/secret.txt')
def load_secret_txt():
    return render_template('secret.html')

@main_bp.route('/config')
def load_config_file():
    return render_template('config.html')

@main_bp.route('/todo.txt')
def load_todo_list():
    return  main_bp.send_static_file('todolist.txt')

@main_bp.route('/Management/')
def load_management():
    return redirect(url_for('main_bp.load_management_login'))


@main_bp.route('/Management/testlogin')
def load_management_login():
    return render_template('login_page_test.html')

# Needs another bruteforce in order to get to the login form.
@main_bp.route('/Management/login_form')
def load_management_admin():
    return redirect(url_for('main_bp.load_admin_login'))

# Here is the admin login page.
@main_bp.route('/Management/login_form/admin_login_v2/login', methods=['GET', 'POST'])
def load_admin_login():
    """Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard."""
  
    form = LoginForm()

    if form.validate_on_submit():
        # check for a specifc email and password
        # in order to avoid SQL injection etc..
        if form.email.data == "admin@eatery.co.il" and form.password.data == "Password1":
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user)
            return redirect(url_for('main_bp.dashboard'))

        flash('Invalid email/password')
        return redirect(url_for('main_bp.load_admin_login'))

    return render_template(
        'admin_login/login.jinja2',
        form=form,
        title='Log in - Eatery Cafe',
        template='login-page',
        body="Log in with your User account."
    )

@main_bp.route('/Management/login_form/admin_login_v2/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation."""

    form = SignupForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            return redirect(url_for('main_bp.load_admin_login'))

        flash('A user already exists with that email address.')
        
    return render_template(
        'admin_login/signup.jinja2',
        title='Create an Account',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )
    
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('main_bp.load_admin_login'))

# loading the dashboard, after login.
@main_bp.route('/Management/login_form/admin_login_v2/dashboard/index.html', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard/index.html')

@main_bp.route('/Management/login_form/admin_login_v2/dashboard/ui-maps.html')
def load_maps():
    return render_template('dashboard/ui-maps.html')

@main_bp.route('/Management/login_form/admin_login_v2/dashboard/ui-icons.html')
@login_required
def load_icons():
    return render_template('dashboard/ui-icons.html')

@main_bp.route('/Management/login_form/admin_login_v2/dashboard/ui-notifications.html')
@login_required
def load_nof():
    return render_template('dashboard/ui-notifications.html')

@main_bp.route('/Management/login_form/admin_login_v2/dashboard/page-user.html')
@login_required
def load_page_user_html():
    return render_template('dashboard/page-user.html')

# ------------------------------------------------------- #
# The Important Part - SSTI - inject payload in order to get the private keys.
@main_bp.route("/Management/login_form/admin_login_v2/dashboard/register", methods=['GET', 'POST'])
def load_register_ssti():
    content = request.args.get("register")
    if content:
        return render_template_string(content)
    return render_template('dashboard/accounts/register.html')


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out."""
    logout_user()
    return redirect(url_for('main_bp.load_admin_login'))