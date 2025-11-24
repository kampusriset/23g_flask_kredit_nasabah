from datetime import datetime
from .. import db

class Pengajuan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nasabah_id = db.Column(db.Integer, db.ForeignKey('nasabah.id'), nullable=False)
    jumlah_pinjaman = db.Column(db.Float, nullable=False)
    tenor = db.Column(db.Integer, nullable=False)  # dalam bulan
    tujuan = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='menunggu')  # menunggu, disetujui, ditolak, dibatalkan, lunas
    catatan = db.Column(db.Text, nullable=True)  # Catatan saat disetujui/ditolak
    tanggal_mulai = db.Column(db.DateTime, nullable=True)  # Tanggal mulai pembayaran (saat disetujui)
    tanggal_survei = db.Column(db.DateTime, nullable=True)  # Tanggal jadwal survei
    status_survei = db.Column(db.String(50), default='belum_dijadwalkan')  # belum_dijadwalkan, dijadwalkan, selesai, dibatalkan
    catatan_survei = db.Column(db.Text, nullable=True)  # Catatan hasil survei
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship sudah ada di Nasabah model

    def __repr__(self):
        return f'<Pengajuan {self.id} status={self.status}>'

    @property
    def is_aktif(self):
        """Check if pengajuan is active (approved and not completed)"""
        return self.status == 'disetujui'

    @property
    def total_pinjaman_dengan_bunga(self):
        """Hitung total pinjaman dengan bunga sederhana 2% per bulan"""
        if not self.is_aktif:
            return 0
        bunga_per_bulan = 0.02  # 2%
        return self.jumlah_pinjaman * (1 + (bunga_per_bulan * self.tenor))

    @property
    def angsuran_per_bulan(self):
        """Hitung angsuran per bulan"""
        if not self.is_aktif or self.tenor == 0:
            return 0
        return self.total_pinjaman_dengan_bunga / self.tenor


class Pembayaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengajuan_id = db.Column(db.Integer, db.ForeignKey('pengajuan.id'), nullable=False)
    bulan_ke = db.Column(db.Integer, nullable=False)  # Bulan ke berapa (1, 2, 3, ...)
    jumlah_bayar = db.Column(db.Float, nullable=False)
    tanggal_jatuh_tempo = db.Column(db.Date, nullable=False)
    tanggal_bayar = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='belum_bayar')  # belum_bayar, sudah_bayar, terlambat
    denda = db.Column(db.Float, default=0)  # Denda keterlambatan
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    pengajuan = db.relationship('Pengajuan', backref=db.backref('pembayaran', lazy=True))

    def __repr__(self):
        return f'<Pembayaran {self.id} bulan_ke={self.bulan_ke} status={self.status}>'

    @property
    def is_terlambat(self):
        """Check if payment is overdue"""
        if self.status == 'sudah_bayar':
            return False
        today = datetime.now().date()
        return today > self.tanggal_jatuh_tempo

    @property
    def hari_terlambat(self):
        """Calculate days overdue"""
        if not self.is_terlambat:
            return 0
        today = datetime.now().date()
        return (today - self.tanggal_jatuh_tempo).days

    @property
    def denda_terbaru(self):
        """Calculate current fine for overdue payment"""
        if not self.is_terlambat:
            return 0
        # Denda 0.1% per hari dari jumlah bayar
        return self.jumlah_bayar * 0.001 * self.hari_terlambat
