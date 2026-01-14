from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from ..models.pengajuan import Pengajuan

bp = Blueprint('notifikasi', __name__, url_prefix='/notifikasi')

@bp.route('/')
@login_required
def index():
    """Display system notifications page"""
    # Get pengajuan menunggu persetujuan
    pengajuan_menunggu = Pengajuan.query.filter_by(status='menunggu').all()

    # Get pengajuan disetujui tapi belum dicairkan
    pengajuan_disetujui = Pengajuan.query.filter_by(status='disetujui').all()

    # For now, we'll show empty list for jatuh tempo since pembayaran model doesn't exist
    jatuh_tempo = []


    return render_template('notifikasi/notifikasi.html',

                         jatuh_tempo=jatuh_tempo,
                         pengajuan_menunggu=pengajuan_menunggu,
                         pengajuan_disetujui=pengajuan_disetujui)


@bp.route('/api/notifications')
@login_required
def api_notifications():
    """API endpoint for notification dropdown"""
    notifications = []
    
    if current_user.role == 'admin':
        # Admin sees pending applications
        pengajuan_menunggu = Pengajuan.query.filter_by(status='menunggu').limit(5).all()
        for p in pengajuan_menunggu:
            notifications.append({
                'title': 'Pengajuan Baru',
                'message': f'Pengajuan dari {p.nasabah.nama if p.nasabah else "Unknown"} menunggu persetujuan',
                'type': 'warning',
                'icon': 'bi-file-earmark-text',
                'url': f'/pengajuan/{p.id}'
            })
    else:
        # Nasabah sees their own application status updates
        if current_user.nasabah:
            pengajuan_list = Pengajuan.query.filter_by(nasabah_id=current_user.nasabah.id).order_by(Pengajuan.tanggal_pengajuan.desc()).limit(5).all()
            for p in pengajuan_list:
                if p.status == 'disetujui':
                    notifications.append({
                        'title': 'Pengajuan Disetujui',
                        'message': f'Pengajuan Rp {p.jumlah_pinjaman:,.0f} telah disetujui',
                        'type': 'success',
                        'icon': 'bi-check-circle',
                        'url': f'/pengajuan/{p.id}'
                    })
                elif p.status == 'ditolak':
                    notifications.append({
                        'title': 'Pengajuan Ditolak',
                        'message': f'Pengajuan Rp {p.jumlah_pinjaman:,.0f} tidak disetujui',
                        'type': 'danger',
                        'icon': 'bi-x-circle',
                        'url': f'/pengajuan/{p.id}'
                    })
    
    return jsonify(notifications)


@bp.route('/api/notifications/count')
@login_required
def api_notifications_count():
    """API endpoint for notification count"""
    count = 0
    
    if current_user.role == 'admin':
        count = Pengajuan.query.filter_by(status='menunggu').count()
    else:
        if current_user.nasabah:
            # Count recent approved/rejected
            count = Pengajuan.query.filter(
                Pengajuan.nasabah_id == current_user.nasabah.id,
                Pengajuan.status.in_(['disetujui', 'ditolak'])
            ).count()
    
    return jsonify({'count': count})
