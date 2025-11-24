import os
import unittest
from werkzeug.security import generate_password_hash

# Use in-memory DB for tests
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app, db
from app.models.user import User
from app.models.nasabah import Nasabah
from app.models.pengajuan import Pengajuan, Pembayaran


class PembayaranFlowsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

        db.drop_all()
        db.create_all()

        # Create admin user
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)

        # Create nasabah user
        nasabah_user = User(username='nasabah1', password=generate_password_hash('nasabah123'), role='nasabah')
        db.session.add(nasabah_user)
        db.session.commit()

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def test_pembayaran_flow_admin(self):
        """Test pembayaran flow as admin"""
        # Login as admin
        r = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Selamat datang', r.data)

        # Create nasabah
        nasabah = Nasabah(nama='John Doe', nik='1234567890123456', alamat='Jl. Test 1',
                         no_telp='081234567890', pekerjaan='Karyawan', penghasilan=5000000)
        db.session.add(nasabah)
        db.session.commit()

        # Create pengajuan
        pengajuan = Pengajuan(nasabah_id=nasabah.id, jumlah_pinjaman=1000000, tenor=12, tujuan='Test')
        db.session.add(pengajuan)
        db.session.commit()

        # Approve pengajuan (this should create pembayaran records)
        r2 = self.client.post(f'/pengajuan/setujui/{pengajuan.id}', data={'catatan': 'Approved'}, follow_redirects=True)
        self.assertEqual(r2.status_code, 200)
        self.assertIn(b'Pengajuan disetujui', r2.data)

        # Check that pembayaran records were created
        pembayaran_list = Pembayaran.query.filter_by(pengajuan_id=pengajuan.id).all()
        self.assertEqual(len(pembayaran_list), 12)  # 12 months

        # Test jadwal pembayaran page
        r3 = self.client.get(f'/pembayaran/pengajuan/{pengajuan.id}')
        self.assertEqual(r3.status_code, 200)
        self.assertIn(b'Jadwal Pembayaran', r3.data)
        self.assertIn(b'John Doe', r3.data)

        # Test bayar function
        first_pembayaran = pembayaran_list[0]
        r4 = self.client.post(f'/pembayaran/bayar/{first_pembayaran.id}', follow_redirects=True)
        self.assertEqual(r4.status_code, 200)
        self.assertIn(b'berhasil dicatat', r4.data)

        # Check that pembayaran status changed
        updated_pembayaran = Pembayaran.query.get(first_pembayaran.id)
        self.assertEqual(updated_pembayaran.status, 'sudah_bayar')
        self.assertIsNotNone(updated_pembayaran.tanggal_bayar)

    def test_pembayaran_flow_nasabah(self):
        """Test pembayaran flow as nasabah"""
        # Login as nasabah
        r = self.client.post('/login', data={'username': 'nasabah1', 'password': 'nasabah123'}, follow_redirects=True)
        self.assertEqual(r.status_code, 200)

        # Create nasabah linked to user
        nasabah = Nasabah(user_id=2, nama='Jane Doe', nik='9876543210987654', alamat='Jl. Test 2',
                         no_telp='081987654321', pekerjaan='Wiraswasta', penghasilan=6000000)
        db.session.add(nasabah)
        db.session.commit()

        # Create pengajuan for this nasabah
        pengajuan = Pengajuan(nasabah_id=nasabah.id, jumlah_pinjaman=2000000, tenor=6, tujuan='Test nasabah')
        db.session.add(pengajuan)
        db.session.commit()

        # Approve pengajuan
        # First logout and login as admin to approve
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})

        r2 = self.client.post(f'/pengajuan/setujui/{pengajuan.id}', data={'catatan': 'Approved for nasabah'}, follow_redirects=True)
        self.assertEqual(r2.status_code, 200)

        # Logout admin and login as nasabah again
        self.client.get('/logout')
        r3 = self.client.post('/login', data={'username': 'nasabah1', 'password': 'nasabah123'}, follow_redirects=True)
        self.assertEqual(r3.status_code, 200)

        # Test jadwal pembayaran page as nasabah
        r4 = self.client.get(f'/pembayaran/pengajuan/{pengajuan.id}')
        self.assertEqual(r4.status_code, 200)
        self.assertIn(b'Jadwal Pembayaran', r4.data)
        self.assertIn(b'Pengajuan Anda', r4.data)

    def test_export_jadwal(self):
        """Test export jadwal pembayaran"""
        # Login as admin
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})

        # Create test data
        nasabah = Nasabah(nama='Export Test', nik='1111222233334444', alamat='Jl. Export',
                         no_telp='081111111111', pekerjaan='Test', penghasilan=5000000)
        db.session.add(nasabah)
        db.session.commit()  # Commit nasabah first

        pengajuan = Pengajuan(nasabah_id=nasabah.id, jumlah_pinjaman=1500000, tenor=3, tujuan='Export test')
        db.session.add(pengajuan)
        db.session.commit()

        # Approve to create pembayaran
        self.client.post(f'/pengajuan/setujui/{pengajuan.id}', data={'catatan': 'For export test'})

        # Test export
        r = self.client.get(f'/pembayaran/export/{pengajuan.id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.mimetype, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename=', r.headers.get('Content-Disposition', ''))

        # Check Excel content (binary data, so we check headers and filename)
        self.assertIn('Export Test', r.headers.get('Content-Disposition', ''))
        self.assertIn('.xlsx', r.headers.get('Content-Disposition', ''))


if __name__ == '__main__':
    unittest.main()
