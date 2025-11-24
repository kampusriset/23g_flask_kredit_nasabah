from datetime import datetime
from .. import db

class Dokumen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengajuan_id = db.Column(db.Integer, db.ForeignKey('pengajuan.id'), nullable=False)
    jenis_dokumen = db.Column(db.String(50), nullable=False)  # ktp, kk, npwp, bpkb
    nama_file = db.Column(db.String(255), nullable=True)  # nama file asli
    path_file = db.Column(db.String(500), nullable=True)  # path penyimpanan file
    keterangan = db.Column(db.Text, nullable=True)  # keterangan opsional
    status = db.Column(db.String(50), default='belum_diupload')  # belum_diupload, sudah_diupload, ditolak
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # user yang upload
    uploaded_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    pengajuan = db.relationship('Pengajuan', backref=db.backref('dokumen', lazy=True))
    uploader = db.relationship('User', backref=db.backref('uploaded_dokumen', lazy=True))

    def __repr__(self):
        return f'<Dokumen {self.jenis_dokumen} pengajuan_id={self.pengajuan_id}>'

    @property
    def is_complete(self):
        """Check if document is uploaded and approved"""
        return self.status == 'sudah_diupload'

    @property
    def jenis_dokumen_display(self):
        """Display name for document type"""
        jenis_map = {
            'ktp': 'KTP',
            'kk': 'Kartu Keluarga',
            'npwp': 'NPWP',
            'bpkb': 'BPKB'
        }
        return jenis_map.get(self.jenis_dokumen, self.jenis_dokumen.upper())
