# SIPINA - Sistem Informasi Kredit Nasabah (Simple Flask App)

Ini adalah contoh aplikasi sederhana SIPINA menggunakan Flask dan SQLite.
Struktur proyek:
- app.py                -> aplikasi Flask (model, route, db)
- templates/            -> HTML templates (Bootstrap CDN)
- static/               -> static files (CSS)

## Cara menjalankan (Windows / Linux / macOS)
1. Pastikan Python 3.10+ terpasang.
2. Ekstrak `sipina_flask.zip`.
3. (opsional) Buat virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
4. Pasang dependensi:
   ```bash
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi:
   ```bash
   python run.py
   ```
  Aplikasi akan berjalan pada http://127.0.0.1:5000

Database SQLite `sipina.db` akan dibuat otomatis di folder proyek saat pertama kali dijalankan.

Fitur sederhana:
- CRUD untuk Nasabah (Customer)
- CRUD untuk Kredit (Loan)
- Menampilkan daftar pembayaran sederhana

Catatan:
- Aplikasi ini dibuat untuk keperluan demo dan pembelajaran.
- Untuk production, gunakan migrasi, autentikasi, validasi form, dan sanitasi input.
