from flask_login import UserMixin
from .. import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='admin')  # admin or nasabah
    foto_profil = db.Column(db.String(255), nullable=True)  # Path to profile photo

    # Relationship to Nasabah
    nasabah = db.relationship('Nasabah', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'
