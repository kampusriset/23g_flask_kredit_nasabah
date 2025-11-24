from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    # Use the project's top-level templates folder to avoid conflicts
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=templates_dir)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu.'

    with app.app_context():
        # Import models so SQLAlchemy knows about them
        from .models import user, nasabah, pengajuan, dokumen
        db.create_all()

        # Seed a default admin user if none exists
        User = user.User
        try:
            if User.query.count() == 0:
                admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            print(f"Error checking users: {e}")
            # Try to create admin anyway
            try:
                admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
                db.session.add(admin)
                db.session.commit()
            except Exception as e2:
                print(f"Error creating admin: {e2}")

    # Import controllers
    from .controllers import auth_controller, nasabah_controller, pengajuan_controller, dashboard_controller, user_controller, info_controller, pembayaran_controller, notifikasi_controller, dokumen_controller

    # Register blueprints
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(nasabah_controller.bp)
    app.register_blueprint(pengajuan_controller.bp)
    app.register_blueprint(dashboard_controller.bp)
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(info_controller.bp)
    app.register_blueprint(pembayaran_controller.bp)
    app.register_blueprint(notifikasi_controller.bp)
    app.register_blueprint(dokumen_controller.bp)

    # Add root route to show landing page
    @app.route('/')
    def landing():
        return render_template('landing.html')

    return app
