-- MySQL Database Schema for SIPINA Application
-- Generated from Flask-SQLAlchemy models
-- MySQL 8.x compatible

CREATE DATABASE IF NOT EXISTS sipina_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE sipina_db;

-- User table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    foto_profil VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Nasabah table
CREATE TABLE nasabah (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    nama VARCHAR(120) NOT NULL,
    nik VARCHAR(20) UNIQUE NOT NULL,
    alamat VARCHAR(255) NOT NULL,
    no_telp VARCHAR(20) UNIQUE NOT NULL,
    pekerjaan VARCHAR(100) NOT NULL,
    penghasilan FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Pengajuan table
CREATE TABLE pengajuan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nasabah_id INT NOT NULL,
    jumlah_pinjaman FLOAT NOT NULL,
    tenor INT NOT NULL,
    tujuan VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'menunggu',
    catatan TEXT,
    tanggal_mulai DATETIME,
    tanggal_survei DATETIME,
    status_survei VARCHAR(50) DEFAULT 'belum_dijadwalkan',
    catatan_survei TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (nasabah_id) REFERENCES nasabah(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dokumen table
CREATE TABLE dokumen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pengajuan_id INT NOT NULL,
    jenis_dokumen VARCHAR(50) NOT NULL,
    nama_file VARCHAR(255),
    path_file VARCHAR(500),
    keterangan TEXT,
    status VARCHAR(50) DEFAULT 'belum_diupload',
    uploaded_by INT,
    uploaded_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pengajuan_id) REFERENCES pengajuan(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Pembayaran table
CREATE TABLE pembayaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pengajuan_id INT NOT NULL,
    bulan_ke INT NOT NULL,
    jumlah_bayar FLOAT NOT NULL,
    tanggal_jatuh_tempo DATE NOT NULL,
    tanggal_bayar DATETIME,
    status VARCHAR(50) DEFAULT 'belum_bayar',
    denda FLOAT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pengajuan_id) REFERENCES pengajuan(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
