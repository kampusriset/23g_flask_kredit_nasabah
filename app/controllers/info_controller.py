from flask import Blueprint, render_template


bp = Blueprint('info', __name__)


@bp.route('/info')

def index():
    return render_template('info/index.html')



@bp.route('/info/layanan')

def layanan():
    return render_template('info/layanan.html')



@bp.route('/info/prosedur')

def prosedur():
    return render_template('info/prosedur.html')



@bp.route('/info/kontak')

def kontak():
    return render_template('info/kontak.html')


