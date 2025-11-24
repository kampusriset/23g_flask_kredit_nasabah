from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from ..models.nasabah import Nasabah
from ..models.pengajuan import Pengajuan
from datetime import datetime, timedelta


bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')

@login_required
def index():
    # If user is not authenticated, redirect to login
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.role == 'nasabah':
        # Dashboard untuk nasabah
        from ..models.pengajuan import Pembayaran

        # Cari nasabah yang terkait dengan user ini
        nasabah = Nasabah.query.filter_by(user_id=current_user.id).first()
        if not nasabah:
            flash('Data nasabah tidak ditemukan. Silakan hubungi admin.', 'warning')
            return redirect(url_for('auth.logout'))

        # Pengajuan milik nasabah ini
        pengajuan_list = Pengajuan.query.filter_by(nasabah_id=nasabah.id).all()
        total_pengajuan = len(pengajuan_list)
        pengajuan_menunggu = len([p for p in pengajuan_list if p.status == 'menunggu'])
        pengajuan_disetujui = len([p for p in pengajuan_list if p.status == 'disetujui'])
        pengajuan_ditolak = len([p for p in pengajuan_list if p.status == 'ditolak'])

        # Total outstanding untuk nasabah ini
        total_outstanding = sum([p.jumlah_pinjaman for p in pengajuan_list if p.status == 'disetujui'])

        # Hitung pembayaran yang sudah dilakukan
        pembayaran_sudah = 0
        pembayaran_belum = 0
        total_denda = 0

        for pengajuan in pengajuan_list:
            if pengajuan.status == 'disetujui':
                pembayaran_list = Pembayaran.query.filter_by(pengajuan_id=pengajuan.id).all()
                pembayaran_sudah += len([p for p in pembayaran_list if p.status == 'sudah_bayar'])
                pembayaran_belum += len([p for p in pembayaran_list if p.status == 'belum_bayar'])
                total_denda += sum([p.denda for p in pembayaran_list])

        # Get pembayaran jatuh tempo untuk nasabah ini
        jatuh_tempo = Pembayaran.query.join(Pengajuan).filter(
            Pengajuan.nasabah_id == nasabah.id,
            Pembayaran.status == 'belum_bayar',
            Pembayaran.tanggal_jatuh_tempo < datetime.now().date()
        ).all()


        return render_template('dashboard/dashboard_nasabah.html',

                               nasabah=nasabah,
                               total_pengajuan=total_pengajuan,
                               pengajuan_menunggu=pengajuan_menunggu,
                               pengajuan_disetujui=pengajuan_disetujui,
                               pengajuan_ditolak=pengajuan_ditolak,
                               total_outstanding=total_outstanding,
                               pembayaran_sudah=pembayaran_sudah,
                               pembayaran_belum=pembayaran_belum,
                               total_denda=total_denda,
                               jatuh_tempo=jatuh_tempo)

    else:
        # Dashboard untuk admin (existing logic)
        total_nasabah = Nasabah.query.count()
        total_pengajuan = Pengajuan.query.count()
        pengajuan_menunggu = Pengajuan.query.filter_by(status='menunggu').count()
        pengajuan_disetujui = Pengajuan.query.filter_by(status='disetujui').count()
        pengajuan_ditolak = Pengajuan.query.filter_by(status='ditolak').count()
        total_outstanding = db.session.query(db.func.coalesce(db.func.sum(Pengajuan.jumlah_pinjaman), 0)).filter(Pengajuan.status == 'disetujui').scalar()

        # Get chart data
        status_counts = {
            'menunggu': pengajuan_menunggu,
            'disetujui': pengajuan_disetujui,
            'ditolak': pengajuan_ditolak
        }

        # Weekly data for bar chart
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        pengajuan_week = Pengajuan.query.filter(Pengajuan.created_at >= week_ago).all()
        daily_counts = {}

        for i in range(7):
            date = week_ago + timedelta(days=i)
            date_str = date.strftime('%a')
            count = len([p for p in pengajuan_week if p.created_at.date() == date.date()])
            daily_counts[date_str] = count


        return render_template('dashboard/dashboard.html',

                               total_nasabah=total_nasabah,
                               total_pengajuan=total_pengajuan,
                               pengajuan_menunggu=pengajuan_menunggu,
                               pengajuan_disetujui=pengajuan_disetujui,
                               pengajuan_ditolak=pengajuan_ditolak,
                               total_outstanding=total_outstanding,
                               status_counts=status_counts,
                               daily_counts=daily_counts)

@bp.route('/analytics')
@login_required
def analytics():
    """Advanced analytics and reporting"""
    # Get all data
    all_pengajuan = Pengajuan.query.all()
    all_nasabah = Nasabah.query.all()

    # Calculate statistics
    if all_pengajuan:
        pengajuan_disetujui = len([p for p in all_pengajuan if p.status == 'disetujui'])
        pengajuan_ditolak = len([p for p in all_pengajuan if p.status == 'ditolak'])
        pengajuan_menunggu = len([p for p in all_pengajuan if p.status == 'menunggu'])
        approval_rate = (pengajuan_disetujui / len(all_pengajuan)) * 100
        rejection_rate = (pengajuan_ditolak / len(all_pengajuan)) * 100
        pending_rate = (pengajuan_menunggu / len(all_pengajuan)) * 100
    else:
        approval_rate = rejection_rate = pending_rate = 0
        pengajuan_disetujui = pengajuan_ditolak = pengajuan_menunggu = 0

    # Loan statistics
    approved_loans = [p for p in all_pengajuan if p.status == 'disetujui']
    if approved_loans:
        avg_loan = sum([p.jumlah_pinjaman for p in approved_loans]) / len(approved_loans)
        max_loan = max([p.jumlah_pinjaman for p in approved_loans])
        min_loan = min([p.jumlah_pinjaman for p in approved_loans])
        total_approved = sum([p.jumlah_pinjaman for p in approved_loans])
    else:
        avg_loan = max_loan = min_loan = total_approved = 0

    # Customer statistics
    if all_nasabah:
        avg_income = sum([n.penghasilan for n in all_nasabah]) / len(all_nasabah)
        max_income = max([n.penghasilan for n in all_nasabah])
        min_income = min([n.penghasilan for n in all_nasabah])
    else:
        avg_income = max_income = min_income = 0

    # Monthly trend data
    months_data = {}
    for i in range(12):
        month_date = datetime.now() - timedelta(days=30*i)
        month_key = month_date.strftime('%B %Y')
        count = len([p for p in all_pengajuan if p.created_at.month == month_date.month and p.created_at.year == month_date.year])
        months_data[month_key] = count

    # Recent applications for table
    pengajuan_list = Pengajuan.query.order_by(Pengajuan.created_at.desc()).limit(10).all()


    return render_template('analytics/analytics.html',

                           approval_rate=round(approval_rate, 1),
                           rejection_rate=round(rejection_rate, 1),
                           pending_rate=round(pending_rate, 1),
                           avg_loan=int(avg_loan),
                           max_loan=int(max_loan),
                           min_loan=int(min_loan),
                           total_approved=int(total_approved),
                           avg_income=int(avg_income),
                           max_income=int(max_income),
                           min_income=int(min_income),
                           total_nasabah=len(all_nasabah),
                           total_pengajuan=len(all_pengajuan),
                           months_data=months_data,
                           pengajuan_list=pengajuan_list,
                           pengajuan_disetujui=pengajuan_disetujui,
                           pengajuan_menunggu=pengajuan_menunggu,
                           pengajuan_ditolak=pengajuan_ditolak)


