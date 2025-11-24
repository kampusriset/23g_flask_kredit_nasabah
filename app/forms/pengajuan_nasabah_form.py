from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PengajuanNasabahForm(FlaskForm):
    jumlah_pinjaman = FloatField('Jumlah Pinjaman (Rp)', validators=[DataRequired(), NumberRange(min=100000)])
    tenor = IntegerField('Tenor (bulan)', validators=[DataRequired(), NumberRange(min=1, max=360)])
    tujuan = TextAreaField('Tujuan Pinjaman', validators=[DataRequired()])
    foto_ktp = FileField('Foto KTP', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Hanya file gambar (JPG, JPEG, PNG) yang diperbolehkan!')])
    submit = SubmitField('Ajukan')
