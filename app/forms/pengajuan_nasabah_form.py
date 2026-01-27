from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import FloatField, IntegerField, TextAreaField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange

class PengajuanNasabahForm(FlaskForm):
    jumlah_pinjaman = FloatField('Jumlah Pinjaman (Rp)', validators=[DataRequired(), NumberRange(min=100000)])
    tenor = IntegerField('Tenor (bulan)', validators=[DataRequired(), NumberRange(min=1, max=360)])
    tujuan = TextAreaField('Tujuan Pinjaman', validators=[DataRequired()])
    rentang_gaji = SelectField('Rentang Pendapatan Per Bulan', choices=[
        ('1000000', 'Rp 1.000.000 - Rp 3.000.000'),
        ('3000000', 'Rp 3.000.000 - Rp 5.000.000'),
        ('5000000', 'Rp 5.000.000 - Rp 10.000.000'),
        ('10000000', 'Rp 10.000.000 - Rp 20.000.000'),
        ('20000000', '> Rp 20.000.000')
    ], validators=[DataRequired()])
    foto_ktp = FileField('Foto KTP', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan!')])
    foto_kk = FileField('Foto Kartu Keluarga (KK)', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Format file harus JPG, PNG, atau PDF!')])
    tempat_kerja = StringField('Nama Tempat Kerja/Instansi', validators=[DataRequired()])
    posisi_pekerjaan = SelectField('Posisi/Jabatan', choices=[
        ('Staff / Karyawan', 'Staff / Karyawan'),
        ('Supervisor / Koordinator', 'Supervisor / Koordinator'),
        ('Manajer / Asisten Manajer', 'Manajer / Asisten Manajer'),
        ('Direktur / Eksekutif', 'Direktur / Eksekutif'),
        ('PNS / TNI / Polri', 'PNS / TNI / Polri'),
        ('Wirausaha / Pemilik Usaha', 'Wirausaha / Pemilik Usaha'),
        ('Profesional', 'Profesional (Dokter, Guru, Dosen, dll)'),
        ('Buruh', 'Buruh / Pekerja Harian'),
        ('ART', 'ART / Asisten Rumah Tangga'),
        ('Freelance', 'Freelance / Pekerja Lepas'),
        ('Lainnya', 'Lainnya')
    ], validators=[DataRequired()])
    foto_selfie = FileField('Foto Selfie (Wajib)', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan!')])
    submit = SubmitField('Ajukan')
