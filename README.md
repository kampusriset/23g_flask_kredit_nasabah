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

### Backend (Server & Logika)

- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) **Flask**: Framework utama (Python 3.11+).
- ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) **MySQL / SQLite**: Sistem penyimpanan data.
- ![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white) **Flask-SQLAlchemy**: ORM Database.
- ![Socket.io](https://img.shields.io/badge/Socket.io-black?style=for-the-badge&logo=socket.io&badgeColor=010101) **Flask-SocketIO**: Komunikasi realtime.

### Frontend (Tampilan & Antarmuka)

- ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white) **Tailwind CSS**: Modern UI Styling.
- ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black) **Jinja2**: Template Engine.
- ![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white) **Chart.js**: Visualisasi statistik.
- ![Bootstrap Icons](https://img.shields.io/badge/bootstrap%20icons-7952B3.svg?style=for-the-badge&logo=bootstrap&logoColor=white) **Bootstrap Icons**: Ikon vektor.

### Utilitas & Keamanan

- ![WTF](https://img.shields.io/badge/Flask--WTF-F7931E?style=for-the-badge&logo=flask&logoColor=white) **Flask-WTF**: Sistem formulir aman.
- ![Login](https://img.shields.io/badge/Flask--Login-000000?style=for-the-badge&logo=flask&logoColor=white) **Flask-Login**: Manajemen otentikasi.

---

## 🔄 Pembaruan Terkini (Januari 2026 - Versi Terbaru)

- **📝 Formulir Kredit Cerdas**: Transformasi total formulir pengajuan dengan input **Rentang Gaji** (dropdown) yang tervalidasi otomatis terhadap limit cicilan (Max 30%). Dilengkapi data pekerjaan detail (Nama Instansi & Posisi Jabatan) untuk analisis kredit yang lebih akurat.
- **📸 Verifikasi Biometrik & Dokumen**: Integrasi fitur **Kamera Selfie Interaktif** di browser dengan panduan wajah dan validasi dokumen fisik (KTP, KK, Bukti Kerja) yang wajib diunggah untuk keamanan data.
- **✅ Sistem Validasi Pembayaran**: Nasabah kini wajib mengunggah **Bukti Transfer/Screenshot** saat konfirmasi pembayaran. Status pembayaran otomatis menjadi _"Menunggu Verifikasi"_, memberikan kontrol penuh bagi Admin untuk memeriksa keaslian transaksi sebelum pelunasan.
- **⚖️ Logika Review Bertingkat**: Admin memiliki akses untuk memverifikasi atau menolak **dokumen individual** dan **bukti pembayaran** secara spesifik, dengan notifikasi status yang jelas (Valid/Ditolak/Pending) pada sisi nasabah.
- **🔔 Smart Notification System**: Penyaringan notifikasi berbasis peran (Role-Based). Nasabah hanya melihat aktivitas akun pribadinya sendiri, menjaga privasi data antar pengguna secara absolut.
- **🌓 Ultra-Adaptive Dark Mode**: Implementasi sistem Mode Gelap yang komprehensif di seluruh interior aplikasi. Dilengkapi dengan _global CSS overrides_ untuk memastikan keterbacaan teks, kontras tabel, dan visibilitas badge status tetap optimal dalam kondisi cahaya rendah. Tema tersimpan secara permanen melalui _localStorage_.
- **💀 Premium Skeleton State loading**: Integrasi pemuatan data berbasis _Skeleton Loader_ menggunakan sistem manager `SIPINA_Loading`. Memberikan pengalaman transisi data yang mulus (zero layout shift) pada dashboard dan sistem notifikasi, meningkatkan persepsi kecepatan aplikasi.
- **🎨 Premium Landing Page Animations**: Implementasi animasi _scroll-triggered_ (staggered), efek shimmer pada kartu fitur, dan transisi navigasi yang responsif untuk kesan pertama yang memukau.
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
