import os
import unittest
from werkzeug.security import generate_password_hash

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app, db
from app.models.user import User
from app.models.nasabah import Nasabah
from app.models.pengajuan import Pengajuan


class ExportAnalyticsValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

        db.drop_all()
        db.create_all()
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

        cls.client = cls.app.test_client()
        # login as admin
        r = cls.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        if r.status_code != 200:
            raise RuntimeError('Unable to login test client')

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def test_nasabah_export_csv(self):
        # create sample nasabah
        n1 = Nasabah(nama='ExportOne', nik='9000111122223333', alamat='A', no_telp='081000', pekerjaan='X', penghasilan=1000000)
        n2 = Nasabah(nama='ExportTwo', nik='9000111122224444', alamat='B', no_telp='082000', pekerjaan='Y', penghasilan=2000000)
        db.session.add_all([n1, n2])
        db.session.commit()

        r = self.client.get('/nasabah/export')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'text/csv', r.content_type.encode() if isinstance(r.content_type, str) else b'')
        self.assertIn(b'Nama', r.data)
        self.assertIn(b'ExportOne', r.data)

    def test_pengajuan_export_csv(self):
        # create nasabah and pengajuan
        nas = Nasabah(nama='PengOne', nik='8000111122223333', alamat='C', no_telp='083000', pekerjaan='Z', penghasilan=1500000)
        db.session.add(nas)
        db.session.commit()
        p = Pengajuan(nasabah_id=nas.id, jumlah_pinjaman=500000, tenor=6, tujuan='Test')
        db.session.add(p)
        db.session.commit()

        r = self.client.get('/pengajuan/export')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'pengajuan_export', r.headers.get('Content-Disposition', '').encode())
        self.assertIn(b'PengOne', r.data)

    def test_analytics_route(self):
        # create pengajuan with different statuses
        nas = Nasabah(nama='AnalyticUser', nik='7000111122223333', alamat='D', no_telp='084000', pekerjaan='A', penghasilan=1200000)
        db.session.add(nas)
        db.session.commit()
        p1 = Pengajuan(nasabah_id=nas.id, jumlah_pinjaman=100000, tenor=12, tujuan='A')
        p2 = Pengajuan(nasabah_id=nas.id, jumlah_pinjaman=200000, tenor=6, tujuan='B')
        db.session.add_all([p1, p2])
        db.session.commit()
        # set statuses
        p1.status = 'disetujui'
        p2.status = 'ditolak'
        db.session.commit()

        r = self.client.get('/analytics')
        self.assertEqual(r.status_code, 200)
        # Check for textual markers from analytics template
        self.assertIn(b'Approval Rate', r.data)
        self.assertIn(b'Rejection Rate', r.data)

    def test_validation_nasabah_missing_required(self):
        before = Nasabah.query.count()
        # missing nama
        data = {'nama': '', 'nik': '1111222233334444', 'alamat': 'X', 'no_telp': '081', 'pekerjaan': 'T', 'penghasilan': '1000'}
        r = self.client.post('/nasabah/tambah', data=data, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        after = Nasabah.query.count()
        self.assertEqual(before, after)

    def test_validation_pengajuan_low_amount(self):
        # ensure nasabah exists
        nas = Nasabah(nama='VUser', nik='6000111122223333', alamat='E', no_telp='085000', pekerjaan='B', penghasilan=900000)
        db.session.add(nas)
        db.session.commit()
        before = Pengajuan.query.count()
        # jumlah_pinjaman below minimum (100000)
        data = {'nasabah_id': str(nas.id), 'jumlah_pinjaman': '5000', 'tenor': '6', 'tujuan': 'small'}
        r = self.client.post('/pengajuan/tambah', data=data, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        after = Pengajuan.query.count()
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
