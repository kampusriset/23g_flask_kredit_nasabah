# 🏦 SIPINA - Sistem Informasi Pinjaman Nasabah

SIPINA adalah platform manajemen pembiayaan dan kredit nasabah modern berbasis web. Aplikasi ini dirancang untuk memudahkan proses pengajuan, analis, hingga pemantauan jadwal pembayaran secara digital dan efisien.

---

## ✨ Fitur Utama

- **📊 Dashboard Interaktif**: Visualisasi data statistik pengajuan untuk Admin dan ringkasan status untuk Nasabah.
- **📝 Manajemen Pengajuan**: Sistem pengajuan pinjaman digital lengkap dengan upload dokumen pendukung (KTP/Dokumen).
- **📉 Advanced Analytics**: Analisis data persetujuan, tren bulanan, dan statistik keuangan bagi administrator.
- **📅 Jadwal Pembayaran Otomatis**: Perhitungan tenor, bunga, dan jadwal jatuh tempo otomatis.
- **📥 Export Data**: Fitur ekspor jadwal pembayaran dan laporan ke format **Excel (.xlsx)**.
- **🔔 Sistem Notifikasi**: Pemberitahuan status pengajuan dan peringatan jatuh tempo.
- **📱 PWA Ready**: Dapat diinstal di perangkat mobile/desktop layaknya aplikasi native.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.11+)
- **ORM**: Flask-SQLAlchemy
- **Database**: SQLite (Default) / MySQL Compatible (Script provided)
- **Frontend**: Jinja2 Templates, Bootstrap 5, Bi-Icons
- **Assets**: CSS & JS Modular (Palette-based)
- **Features**: Progressive Web App (PWA)

---

## 🚀 Cara Menjalankan

### 1. Persiapan Lingkungan

Pastikan Anda memiliki Python 3.11 atau lebih baru.

```powershell
# Buat Virtual Environment
python -m venv venv

# Aktifkan venv (Windows)
.\venv\Scripts\activate

# Aktifkan venv (macOS/Linux)
source venv/bin/activate
```

### 2. Instalasi Dependensi

```powershell
pip install -r requirements.txt
```

### 3. Konfigurasi Database

Aplikasi menggunakan SQLite secara default untuk kemudahan Setup.

- File database utama: `instance/sipina.db`
- Template SQL (MySQL): `instance/database.sql`

### 4. Menjalankan Aplikasi

```powershell
python run.py
```

Akses melalui browser di: `http://127.0.0.1:5000`

---

## 📁 Struktur Proyek

```text
aplikasi_sipina/
├── app/
│   ├── controllers/    # Logika navigasi & route
│   ├── models/         # Skema database
│   ├── forms/          # Validasi formulir (Flask-WTF)
│   ├── static/         # Aset CSS, JS, Gambar & PWA
│   └── templates/      # File HTML (Jinja2)
├── dokumentasi/        # Panduan & laporan implementasi
├── instance/           # Data SQLite & SQL Script
└── run.py              # Entry point aplikasi
```

---

## 👤 Akun Demo Default

- **Role Admin**: Username: `admin` | Password: `admin123`

---

_Dikembangkan untuk efisiensi sistem administrasi kredit nasabah._
