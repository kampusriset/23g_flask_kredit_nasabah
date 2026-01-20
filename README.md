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

- **🌓 Ultra-Adaptive Dark Mode**: Implementasi sistem Mode Gelap yang komprehensif di seluruh interior aplikasi. Dilengkapi dengan _global CSS overrides_ untuk memastikan keterbacaan teks, kontras tabel, dan visibilitas badge status tetap optimal dalam kondisi cahaya rendah. Tema tersimpan secara permanen melalui _localStorage_.
- **💀 Premium Skeleton State loading**: Integrasi pemuatan data berbasis _Skeleton Loader_ menggunakan sistem manager `SIPINA_Loading`. Memberikan pengalaman transisi data yang mulus (zero layout shift) pada dashboard dan sistem notifikasi, meningkatkan persepsi kecepatan aplikasi.
- **💎 Refined Dark Glassmorphism**: Pengaplikasian efek _Frosted Glass_ yang lebih dalam pada kartu dashboard khusus untuk mode gelap, memberikan estetika visual yang modern dan eksklusif.
- **✨ High-Contrast UI Overrides**: Optimalisasi elemen UI di seluruh modul (Daftar Pengajuan & Manajemen User) untuk mode gelap, termasuk pembaharuan otomatis warna input form, dropdown, dan penetrasi teks putih pada elemen-elemen berkontras rendah.
- **🎨 Premium Landing Page Animations**: Implementasi animasi _scroll-triggered_ (staggered), efek shimmer pada kartu fitur, dan transisi navigasi yang responsif untuk kesan pertama yang memukau.
- **💳 Payment Gateway Simulation**: Pilihan metode pembayaran modern (VA & QRIS) dengan instruksi interaktif untuk memudahkan simulasi transaksi cicilan nasabah.
- **📱 Mobile-First UX Architecture**: Optimalisasi navigasi bawah (bottom-nav) dan transformasi tabel otomatis ke mode kartu pada perangkat mobile untuk penggunaan satu tangan yang lebih nyaman.

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
