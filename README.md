# 🏦 SIPINA - Sistem Informasi Pinjaman Nasabah

SIPINA adalah platform manajemen pembiayaan dan kredit nasabah modern berbasis web. Aplikasi ini dirancang untuk memudahkan proses pengajuan, analis, hingga pemantauan jadwal pembayaran secara digital dan efisien.

---

## ✨ Fitur Utama

- **🎨 Modern UI/UX**: Desain antarmuka baru yang premium menggunakan **Tailwind CSS**.
- **📊 Dashboard Interaktif**: Visualisasi data statistik pengajuan untuk Admin dan ringkasan status untuk Nasabah.
- **📝 Manajemen Pengajuan**: Sistem pengajuan kredit digital dengan validasi dokumen otomatis dan pelacakan status realtime.
- **📉 Advanced Analytics**: Analisis data persetujuan, tren bulanan, dan statistik keuangan berbasis grafik.
- **📅 Jadwal Pembayaran**: Kalkulasi tenor otomatis dan tabel pembayaran yang responsif.
- **💬 Realtime Live Chat**: Fitur bantuan langsung antara Nasabah dan Admin menggunakan teknologi **Socket.io**.
- **🔔 Sistem Notifikasi**: Pemberitahuan realtime berbasis dropdown untuk status pengajuan dan aktivitas akun.
- **⚡ Interactive Landing Page**: Halaman muka yang dinamis dengan efek parallax, animasi scroll, dan counter statistik.
- **👤 Profile Management**: Fitur pengaturan akun lengkap termasuk unggah foto profil dan perubahan keamanan.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.11+)
- **Database**: SQLite (Development) / MySQL Ready
- **Frontend**: Tailwind CSS (CDN), Jinja2 Templates
- **Icons**: Bootstrap Icons (Bi-Icons)
- **Framework & Libraries**:
  - Flask-Login (Authentication)
  - Flask-SQLAlchemy (ORM)
  - Flask-SocketIO (Realtime Chat)
  - Flask-WTF (Form Handling & Validation)
  - Chart.js (Data Visualization)

---

## 🔄 Pembaruan Terkini (Januari 2026)

- **Total UI Overhaul**: Migrasi total dari Bootstrap ke **Tailwind CSS** untuk tampilan yang lebih bersih, modern, dan responsif.
- **Real-time Live Chat**: Implementasi fitur chat bantuan langsung dengan sistem room dan tracking pesan yang efisien.
- **Advanced Profile Systems**: Halaman edit profil mandiri dengan dukungan unggah foto (Avatar) dan manajemen keamanan user.
- **Dynamic Topbar**: Integrasi dropdown notifikasi dan profil yang fungsional untuk memudahkan navigasi user.
- **Smooth Content Animations**: Penerapan efek parallax dan Intersection Observer API untuk animasi landing page yang interaktif.
- **Code Optimization**: Sinkronisasi `.gitignore` untuk keamanan data sensitif dan refactoring SocketIO events.

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
