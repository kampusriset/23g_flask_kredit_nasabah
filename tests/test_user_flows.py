import os
import unittest
from werkzeug.security import generate_password_hash

# Ensure factory uses in-memory DB for tests
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app, db
from app.models.user import User


class UserFlowsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

        # fresh schema
        db.drop_all()
        db.create_all()
        # seed admin
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

        cls.client = cls.app.test_client()
        # Log in as admin for protected routes
        login_resp = cls.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        if login_resp.status_code != 200:
            raise RuntimeError('Unable to login test client as admin')

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def test_add_user_success(self):
        # GET form
        resp = self.client.get('/users/tambah')
        self.assertEqual(resp.status_code, 200)

        # POST valid data
        data = {'username': 'testuser', 'password': 'secret123', 'role': 'petugas'}
        resp = self.client.post('/users/tambah', data=data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'User berhasil ditambahkan', resp.data)

        u = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(u)
        self.assertEqual(u.role, 'petugas')

    def test_add_user_duplicate(self):
        # Create existing user
        u = User(username='dupe', password=generate_password_hash('pass123'), role='petugas')
        db.session.add(u)
        db.session.commit()

        # Attempt to create again
        resp = self.client.post('/users/tambah', data={'username': 'dupe', 'password': 'another123', 'role': 'petugas'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Username sudah terdaftar', resp.data)

    def test_edit_user_no_password(self):
        # Create user to edit
        u = User(username='editme', password=generate_password_hash('oldpass'), role='petugas')
        db.session.add(u)
        db.session.commit()
        uid = u.id
        old_hash = u.password

        # Submit edit without password
        resp = self.client.post(f'/users/edit/{uid}', data={'username': 'edited', 'password': '', 'role': 'petugas'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'User berhasil diperbarui', resp.data)

        u2 = User.query.get(uid)
        self.assertEqual(u2.username, 'edited')
        # password should remain unchanged
        self.assertEqual(u2.password, old_hash)


if __name__ == '__main__':
    unittest.main()
