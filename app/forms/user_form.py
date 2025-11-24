from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, NumberRange, Optional
from ..models.user import User
from ..models.nasabah import Nasabah


class UserForm(FlaskForm):
    # User account fields
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[Optional()])
    confirm_password = PasswordField('Konfirmasi Password', validators=[Optional(), EqualTo('password', message='Password tidak cocok')])
    role = SelectField('Role', choices=[('admin','Admin'), ('nasabah','Nasabah')], validators=[DataRequired()])

    # Nasabah fields (optional for admin, required for nasabah)
    nama = StringField('Nama Lengkap', validators=[Optional(), Length(min=1, max=120)])
    nik = StringField('NIK', validators=[Optional(), Length(min=16, max=20)])
    alamat = TextAreaField('Alamat', validators=[Optional()])
    no_telp = StringField('No. Telepon', validators=[Optional(), Length(min=10, max=20)])
    pekerjaan = StringField('Pekerjaan', validators=[Optional(), Length(min=1, max=100)])
    penghasilan = FloatField('Penghasilan (Rp)', validators=[Optional(), NumberRange(min=0)])

    submit = SubmitField('Simpan')

    def validate_username(self, field):
        if field.data:
            query = User.query.filter_by(username=field.data)
            if query.first():
                raise ValidationError('Username sudah terdaftar. Pilih username lain.')

    def validate_nik(self, field):
        if field.data:
            query = Nasabah.query.filter_by(nik=field.data)
            if query.first():
                raise ValidationError('NIK sudah terdaftar. Gunakan NIK yang berbeda.')

    def validate_no_telp(self, field):
        if field.data:
            query = Nasabah.query.filter_by(no_telp=field.data)
            if query.first():
                raise ValidationError('No. Telepon sudah terdaftar. Gunakan no. telepon yang berbeda.')
