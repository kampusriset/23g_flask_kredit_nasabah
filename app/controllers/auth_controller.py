from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db, login_manager
from ..models.user import User
from ..models.nasabah import Nasabah
from ..forms.login_form import LoginForm
from ..forms.register_form import RegisterForm

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        flash('Username atau password salah.', 'danger')

    return render_template('auth/login.html', form=form)

# Seed admin user if none exists
@bp.before_app_first_request
def seed_admin():
    from .. import db
    from ..models.user import User
    from werkzeug.security import generate_password_hash

    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Create user account
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password, role='nasabah')
        db.session.add(user)
        db.session.flush()  # Get user ID without committing

        # Create nasabah record
        nasabah = Nasabah(
            user_id=user.id,
            nama=form.nama.data,
            nik=form.nik.data,
            alamat=form.alamat.data,
            no_telp=form.no_telp.data,
            pekerjaan=form.pekerjaan.data,
            penghasilan=form.penghasilan.data
        )
        db.session.add(nasabah)
        db.session.commit()

        flash('Akun nasabah berhasil dibuat! Silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


