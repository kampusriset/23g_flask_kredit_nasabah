from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional


class PengajuanActionForm(FlaskForm):
    catatan = TextAreaField('Catatan', validators=[Optional()])
    submit = SubmitField('Simpan')
