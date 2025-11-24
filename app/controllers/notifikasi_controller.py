from flask import Blueprint, render_template
from flask_login import login_required
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


