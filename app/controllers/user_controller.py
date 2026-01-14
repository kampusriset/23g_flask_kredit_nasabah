from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.security import generate_password_hash
from .. import db
from ..models.user import User
from ..models.nasabah import Nasabah
from ..forms.user_form import UserForm
from sqlalchemy.exc import IntegrityError
from wtforms.validators import DataRequired, Length, NumberRange

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/')
@login_required
def index():
    users = User.query.order_by(User.id.asc()).all()
    total = len(users)

    return render_template('user/users.html', users=users, total=total)



@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    form = UserForm()
    # For the 'tambah' view, require password at the form-validator level
    if request.method == 'POST':
        # replace the password validators dynamically so WTForms enforces it
        form.password.validators = [DataRequired(message='Password wajib diisi.'), Length(min=6, message='Minimal 6 karakter')]
        if form.role.data == 'nasabah':
            # Make nasabah fields required for nasabah role
            form.nama.validators = [DataRequired(message='Nama wajib diisi.'), Length(min=1, max=120)]
            form.nik.validators = [DataRequired(message='NIK wajib diisi.'), Length(min=16, max=20)]
            form.alamat.validators = [DataRequired(message='Alamat wajib diisi.')]
            form.no_telp.validators = [DataRequired(message='No. Telepon wajib diisi.'), Length(min=10, max=20)]
            form.pekerjaan.validators = [DataRequired(message='Pekerjaan wajib diisi.'), Length(min=1, max=100)]
            form.penghasilan.validators = [DataRequired(message='Penghasilan wajib diisi.'), NumberRange(min=0)]
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed, role=form.role.data)
        db.session.add(user)
        db.session.flush()  # Get user ID

        if form.role.data == 'nasabah':
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

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Username sudah terdaftar. Pilih username lain.', 'danger')
            return render_template('user/user_form.html', form=form, action='Tambah')

        flash('User berhasil ditambahkan.', 'success')
        return redirect(url_for('user.index'))
    return render_template('user/user_form.html', form=form, action='Tambah')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    # don't populate password field
    form.password.data = ''
    form.confirm_password.data = ''

    # Populate nasabah fields if user has nasabah record
    if user.nasabah:
        form.nama.data = user.nasabah.nama
        form.nik.data = user.nasabah.nik
        form.alamat.data = user.nasabah.alamat
        form.no_telp.data = user.nasabah.no_telp
        form.pekerjaan.data = user.nasabah.pekerjaan
        form.penghasilan.data = user.nasabah.penghasilan

    if form.validate_on_submit():
        user.username = form.username.data
        user.role = form.role.data
        if form.password.data:
            if len(form.password.data) < 6:
                flash('Password minimal 6 karakter.', 'danger')

                return render_template('user/user_form.html', form=form, action='Edit')

            user.password = generate_password_hash(form.password.data)

        if form.role.data == 'nasabah':
            if user.nasabah:
                # Update existing nasabah record
                user.nasabah.nama = form.nama.data
                user.nasabah.nik = form.nik.data
                user.nasabah.alamat = form.alamat.data
                user.nasabah.no_telp = form.no_telp.data
                user.nasabah.pekerjaan = form.pekerjaan.data
                user.nasabah.penghasilan = form.penghasilan.data
            else:
                # Create new nasabah record
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
        elif user.nasabah:
            # If role changed from nasabah to admin, remove nasabah record
            db.session.delete(user.nasabah)

        db.session.commit()
        flash('User berhasil diperbarui.', 'success')
        return redirect(url_for('user.index'))

    return render_template('user/user_form.html', form=form, action='Edit')



@bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    if id == 1:
        # protect first admin in case it's seeded
        flash('User ini tidak dapat dihapus.', 'danger')
        return redirect(url_for('user.index'))
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus.', 'success')
    return redirect(url_for('user.index'))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from flask_login import current_user
    import os
    from werkzeug.utils import secure_filename
    
    user = User.query.get_or_404(current_user.id)
    
    if request.method == 'POST':
        # Update password if provided
        new_password = request.form.get('password')
        if new_password:
            if len(new_password) < 6:
                flash('Password minimal 6 karakter.', 'danger')
                return redirect(url_for('user.edit_profile'))
            user.password = generate_password_hash(new_password)
        
        # Update profile photo if uploaded
        if 'foto_profil' in request.files:
            file = request.files['foto_profil']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Create unique filename
                ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
                new_filename = f"profile_{user.id}.{ext}"
                upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app', 'static', 'uploads', 'profiles')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, new_filename)
                file.save(filepath)
                user.foto_profil = f"uploads/profiles/{new_filename}"
        
        # Update nasabah info if applicable
        if user.role == 'nasabah' and user.nasabah:
            user.nasabah.nama = request.form.get('nama', user.nasabah.nama)
            user.nasabah.alamat = request.form.get('alamat', user.nasabah.alamat)
            user.nasabah.no_telp = request.form.get('no_telp', user.nasabah.no_telp)
        
        db.session.commit()
        flash('Profil berhasil diperbarui.', 'success')
        return redirect(url_for('user.edit_profile'))
    
    return render_template('user/edit_profile.html', user=user)
