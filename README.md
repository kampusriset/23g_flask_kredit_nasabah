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

## 🔄 Pembaruan Terkini (Januari 2026 - Versi Terbaru)

- **💳 Integrated Payment Gateway Simulation**: Implementasi fitur pilihan metode pembayaran untuk cicilan. Nasabah kini dapat memilih antara **Transfer Virtual Account** (dengan nomor VA otomatis) atau **QRIS Scan-to-Pay** yang dilengkapi dengan instruksi pembayaran langkah-demi-langkah.
- **✨ Immersive Handshake Experience**: Redesain total Landing Page dengan mengadopsi _pervasive background image_ (tangan berjabat) yang terlihat di seluruh halaman. Menggunakan teknik **Glassmorphism** tingkat lanjut (20px blur) pada kartu fitur agar konten tetap terbaca jelas namun tetap mempertahankan estetika latar belakang yang luas.
- **🛠️ UI Simplification & Security**: Penghapusan fitur pencarian global pada Top Bar untuk tampilan yang lebih minimalis. Membatasi visibilitas kolom "Aksi" pada tabel pembayaran hanya untuk nasabah, guna menjaga integritas data dari sisi administratif (Admin hanya dapat memantau).
- **📈 Enhanced Credit Intelligence**: Perbaikan bug pada statistik nasabah di halaman profil serta penambahan metrik baru seperti total dana yang disetujui, rasio persetujuan pengajuan, dan total limit pinjaman aktif.
- **🇮🇩 Indonesian Locale Optimization**: Penyesuaian abreviasi nominal keuangan dari format internasional ("k" & "M") menjadi lokal (**"jt"**) pada seluruh bagian dashboard, analytics, dan rincian angsuran untuk kenyamanan pembacaan pengguna.
- **Profile & Security**: Sistem edit profil mandiri dengan dukungan foto profil (Avatar), manajemen keamanan user, serta fitur **Hapus Akun dan Foto**.
- **Mobile-First UX**: Penambahan Bottom Navigation khusus perangkat mobile dan optimasi tabel ke bentuk kartu (Card Mode) untuk akses yang lebih intuitif di layar kecil.

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
