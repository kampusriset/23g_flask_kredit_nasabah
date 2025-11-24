from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from ..models.nasabah import Nasabah
from ..models.user import User

class NasabahForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired(), Length(min=1, max=120)])
    nik = StringField('NIK', validators=[DataRequired(), Length(min=16, max=20)])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    no_telp = StringField('No. Telepon', validators=[DataRequired(), Length(min=10, max=20)])
    pekerjaan = StringField('Pekerjaan', validators=[DataRequired(), Length(min=1, max=100)])
    penghasilan = FloatField('Penghasilan (Rp)', validators=[DataRequired(), NumberRange(min=0)])
    username = StringField('Username', validators=[Optional(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    user_id = SelectField('User Account', coerce=int, validators=[Optional()], choices=[])
    submit = SubmitField('Simpan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nasabah_id = kwargs.get('nasabah_id', None)

    def validate_nik(self, field):
        if field.data:
            query = Nasabah.query.filter_by(nik=field.data)
            if self.nasabah_id:
                query = query.filter(Nasabah.id != self.nasabah_id)
            if query.first():
                raise ValidationError('NIK sudah terdaftar. Gunakan NIK yang berbeda.')

    def validate_no_telp(self, field):
        if field.data:
            query = Nasabah.query.filter_by(no_telp=field.data)
            if self.nasabah_id:
                query = query.filter(Nasabah.id != self.nasabah_id)
            if query.first():
                raise ValidationError('No. Telepon sudah terdaftar. Gunakan no. telepon yang berbeda.')

    def validate_username(self, field):
        if field.data:
            query = User.query.filter_by(username=field.data)
            # For edit mode, exclude current user's username if it exists
            if self.nasabah_id:
                current_nasabah = Nasabah.query.get(self.nasabah_id)
                if current_nasabah and current_nasabah.user_id:
                    current_user = User.query.get(current_nasabah.user_id)
                    if current_user and current_user.username == field.data:
                        return  # Allow current username
            if query.first():
                raise ValidationError('Username sudah terdaftar. Pilih username lain.')
