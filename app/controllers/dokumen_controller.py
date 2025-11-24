import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .. import db
from ..models.dokumen import Dokumen
from ..models.pengajuan import Pengajuan
from datetime import datetime

bp = Blueprint('dokumen', __name__, url_prefix='/dokumen')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/pengajuan/<int:pengajuan_id>')
@login_required
def index(pengajuan_id):
    """Halaman kelola dokumen untuk pengajuan tertentu"""
    pengajuan = Pengajuan.query.options(db.joinedload(Pengajuan.nasabah)).get_or_404(pengajuan_id)

    # Check permission - only admin can access
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'danger')
        return redirect(url_for('dashboard.index'))

    # Get existing documents
    dokumen_list = Dokumen.query.filter_by(pengajuan_id=pengajuan_id).all()

    # Create document types that should exist
    required_docs = ['ktp', 'kk', 'npwp', 'bpkb']
    existing_docs = {doc.jenis_dokumen: doc for doc in dokumen_list}

    # Create missing documents with default status
    for doc_type in required_docs:
        if doc_type not in existing_docs:
            new_doc = Dokumen(
                pengajuan_id=pengajuan_id,
                jenis_dokumen=doc_type,
                status='belum_diupload'
            )
            db.session.add(new_doc)

    db.session.commit()

    # Refresh document list
    dokumen_list = Dokumen.query.filter_by(pengajuan_id=pengajuan_id).all()

    return render_template('dokumen/index.html',
                         pengajuan=pengajuan,
                         dokumen_list=dokumen_list)

@bp.route('/upload/<int:dokumen_id>', methods=['POST'])
@login_required
def upload(dokumen_id):
    """Upload dokumen"""
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses untuk mengupload dokumen.', 'danger')
        return redirect(url_for('dashboard.index'))

    dokumen = Dokumen.query.get_or_404(dokumen_id)

    if 'file' not in request.files:
        flash('Tidak ada file yang dipilih.', 'danger')
        return redirect(url_for('dokumen.index', pengajuan_id=dokumen.pengajuan_id))

    file = request.files['file']
    keterangan = request.form.get('keterangan', '')

    if file.filename == '':
        flash('Tidak ada file yang dipilih.', 'danger')
        return redirect(url_for('dokumen.index', pengajuan_id=dokumen.pengajuan_id))

    if file and allowed_file(file.filename):
        # Create upload directory if not exists
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'dokumen')
        os.makedirs(upload_dir, exist_ok=True)

        # Secure filename
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{dokumen.jenis_dokumen}_{dokumen.pengajuan_id}_{timestamp}_{filename}"

        # Save file
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        # Update document record
        dokumen.nama_file = file.filename  # original filename
        dokumen.path_file = f"uploads/dokumen/{filename}"  # relative path for web access
        dokumen.keterangan = keterangan
        dokumen.status = 'sudah_diupload'
        dokumen.uploaded_by = current_user.id
        dokumen.uploaded_at = datetime.utcnow()

        db.session.commit()

        flash(f'Dokumen {dokumen.jenis_dokumen_display} berhasil diupload.', 'success')
    else:
        flash('Format file tidak didukung. Gunakan PDF, JPG, JPEG, atau PNG.', 'danger')

    return redirect(url_for('dokumen.index', pengajuan_id=dokumen.pengajuan_id))

@bp.route('/delete/<int:dokumen_id>', methods=['POST'])
@login_required
def delete(dokumen_id):
    """Hapus dokumen"""
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses untuk menghapus dokumen.', 'danger')
        return redirect(url_for('dashboard.index'))

    dokumen = Dokumen.query.get_or_404(dokumen_id)

    # Delete physical file if exists
    if dokumen.path_file:
        file_path = os.path.join(current_app.root_path, 'static', dokumen.path_file)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Reset document status
    dokumen.nama_file = None
    dokumen.path_file = None
    dokumen.keterangan = None
    dokumen.status = 'belum_diupload'
    dokumen.uploaded_by = None
    dokumen.uploaded_at = None

    db.session.commit()

    flash(f'Dokumen {dokumen.jenis_dokumen_display} berhasil dihapus.', 'success')
    return redirect(url_for('dokumen.index', pengajuan_id=dokumen.pengajuan_id))

@bp.route('/view/<int:dokumen_id>')
@login_required
def view(dokumen_id):
    """View dokumen"""
    dokumen = Dokumen.query.get_or_404(dokumen_id)

    if not dokumen.path_file:
        flash('Dokumen tidak ditemukan.', 'danger')
        return redirect(url_for('dokumen.index', pengajuan_id=dokumen.pengajuan_id))

    # Return file for viewing/downloading
    from flask import send_from_directory
    file_path = os.path.join(current_app.root_path, 'static', 'uploads', 'dokumen')
    filename = os.path.basename(dokumen.path_file)

    return send_from_directory(file_path, filename, as_attachment=False)

