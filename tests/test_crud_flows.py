import os
import unittest
from werkzeug.security import generate_password_hash

# Use in-memory DB for tests
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app, db
from app.models.user import User
from app.models.nasabah import Nasabah
from app.models.pengajuan import Pengajuan


class CrudFlowsTest(unittest.TestCase):
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

    def test_login_logout_flow(self):
        # Already logged in from setUpClass, logout then login again
        r = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Login', r.data)

        r2 = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(r2.status_code, 200)
        self.assertIn(b'Selamat datang', r2.data)

    def test_nasabah_crud(self):
        # Create nasabah
        data = {
            'nama': 'Budi Santoso',
            'nik': '1234567890123456',
            'alamat': 'Jl. Merdeka 1',
            'no_telp': '081234567890',
            'pekerjaan': 'Karyawan',
            'penghasilan': '5000000'
        }
        r = self.client.post('/nasabah/tambah', data=data, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Nasabah berhasil ditambahkan', r.data)

        n = Nasabah.query.filter_by(nik='1234567890123456').first()
        self.assertIsNotNone(n)

        # Edit nasabah
        r2 = self.client.post(f'/nasabah/edit/{n.id}', data={
            'nama': 'Budi S.', 'nik': n.nik, 'alamat': n.alamat, 'no_telp': n.no_telp, 'pekerjaan': n.pekerjaan, 'penghasilan': '6000000'
        }, follow_redirects=True)
        self.assertEqual(r2.status_code, 200)
        self.assertIn(b'Nasabah berhasil diperbarui', r2.data)
        n2 = Nasabah.query.get(n.id)
        self.assertEqual(n2.nama, 'Budi S.')
        self.assertEqual(int(n2.penghasilan), 6000000)

        # Delete nasabah
        r3 = self.client.post(f'/nasabah/hapus/{n.id}', follow_redirects=True)
        self.assertEqual(r3.status_code, 200)
        self.assertIn(b'Nasabah berhasil dihapus', r3.data)
        self.assertIsNone(Nasabah.query.get(n.id))

    def test_pengajuan_create_and_actions(self):
        # Ensure a nasabah exists
        nasabah = Nasabah(nama='Siti', nik='1111222233334444', alamat='Jl. A', no_telp='0811111111', pekerjaan='Wiraswasta', penghasilan=7000000)
        db.session.add(nasabah)
        db.session.commit()

        # Create pengajuan
        data = {'nasabah_id': str(nasabah.id), 'jumlah_pinjaman': '1000000', 'tenor': '12', 'tujuan': 'Modal usaha'}
        r = self.client.post('/pengajuan/tambah', data=data, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Pengajuan berhasil diajukan', r.data)

        p = Pengajuan.query.filter_by(nasabah_id=nasabah.id).first()
        self.assertIsNotNone(p)
        self.assertEqual(p.status, 'menunggu')

        # Approve pengajuan
        r2 = self.client.post(f'/pengajuan/setujui/{p.id}', data={'catatan': 'Dokumen lengkap'}, follow_redirects=True)
        self.assertEqual(r2.status_code, 200)
        self.assertIn(b'Pengajuan disetujui', r2.data)
        p2 = Pengajuan.query.get(p.id)
        self.assertEqual(p2.status, 'disetujui')
        self.assertEqual(p2.catatan, 'Dokumen lengkap')

        # Create another nasabah for second pengajuan (to test limit per borrower)
        nasabah2 = Nasabah(nama='Ahmad', nik='5555666677778888', alamat='Jl. B', no_telp='0822222222', pekerjaan='Pegawai', penghasilan=8000000)
        db.session.add(nasabah2)
        db.session.commit()

        # Create another pengajuan with different nasabah and reject
        data2 = {'nasabah_id': str(nasabah2.id), 'jumlah_pinjaman': '2000000', 'tenor': '24', 'tujuan': 'Renovasi'}
        r3 = self.client.post('/pengajuan/tambah', data=data2, follow_redirects=True)
        self.assertIn(b'Pengajuan berhasil diajukan', r3.data)
        p_new = Pengajuan.query.filter_by(jumlah_pinjaman=2000000).first()
        self.assertIsNotNone(p_new)

        r4 = self.client.post(f'/pengajuan/tolak/{p_new.id}', data={'catatan': 'Skor kredit rendah'}, follow_redirects=True)
        self.assertEqual(r4.status_code, 200)
        self.assertIn(b'Pengajuan ditolak', r4.data)
        p_rej = Pengajuan.query.get(p_new.id)
        self.assertEqual(p_rej.status, 'ditolak')
        self.assertEqual(p_rej.catatan, 'Skor kredit rendah')


if __name__ == '__main__':
    unittest.main()
