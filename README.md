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

- **Mobile-First Optimization**: Implementasi **Bottom Navigation Bar** khusus perangkat mobile untuk kemudahan akses utama (Dashboard, Pengajuan, Profil) secara cepat.
- **Responsive Data Tables**: Transformasi otomatis tabel data (Nasabah & Pengajuan) menjadi tampilan **"Card Mode"** pada layar kecil untuk pembacaan informasi yang lebih intuitif tanpa horizontal scroll.
- **Immersive Hero Experience**: Penyesuaian Landing Page menjadi _full-screen immersion_ (100dvh) dengan background kustom yang tetap proporsional dan estetis di layar mobile.
- **Smart Navbar & Menu**: Integrasi navbar transparan yang beradaptasi secara dinamis saat di-scroll, lengkap dengan desain **Custom 2-Line Burger Menu** berwarna putih kontras.
- **Premium UI Refinements**: Optimasi tata letak grid statistik (2 kolom di mobile), penyelarasan konten tengah, serta perbaikan _padding_ dan _margin_ global untuk pengalaman pengguna yang lebih halus.
- **Advanced Profile Systems**: Halaman edit profil mandiri dengan dukungan unggah foto (Avatar), manajemen keamanan user, serta fitur **Hapus Akun** dan **Hapus Foto Profil**.

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
