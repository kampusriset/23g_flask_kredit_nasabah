from datetime import datetime
from .. import db

class Nasabah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Link to User for nasabah role
    nama = db.Column(db.String(120), nullable=False)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    alamat = db.Column(db.String(255), nullable=False)
    no_telp = db.Column(db.String(20), unique=True, nullable=False)
    pekerjaan = db.Column(db.String(100), nullable=False)
    penghasilan = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    pengajuans = db.relationship('Pengajuan', backref='nasabah', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Nasabah {self.nama}>'
