# Mengelola Landing Page melalui Django Admin

Landing page Padi Emas Nusantara sekarang menggunakan konten dari database sehingga teks dan gambar dapat diubah tanpa mengedit HTML.

## 1. Aktifkan database

```bash
python manage.py migrate
```

Jika belum mempunyai akun administrator:

```bash
python manage.py createsuperuser
```

## 2. Buka Admin

```text
http://127.0.0.1:8000/admin/
```

Atau melalui ngrok/domain:

```text
https://DOMAIN-ANDA/admin/
```

## 3. Menu yang tersedia

### Konten Landing Page
Mengatur konten global:
- Logo
- Favicon
- Judul website dan tagline
- Meta description
- Hero: eyebrow, judul, deskripsi, gambar, slogan
- Tentang Kami: judul, dua paragraf, gambar, quote
- Statistik 3 kartu
- Banner Sistem Manajemen Pertanian
- Judul tiap section
- CTA
- Alamat, telepon, email
- Instagram, YouTube, Facebook, LinkedIn
- Footer dan copyright

### Highlight Hero
Mengatur 4 kartu highlight pada area bawah hero. Bisa tambah/hapus, ubah icon, teks, urutan dan aktif/nonaktif.

### Kegiatan
Mengatur kartu kegiatan pertanian. Bisa tambah/hapus, ubah icon, teks, urutan dan aktif/nonaktif.

### Fasilitas
Mengatur kartu fasilitas sekaligus upload gambar fasilitas.

### Galeri
Mengupload foto kegiatan sebanyak yang diperlukan. `order` menentukan urutan tampil dan `is_active` menentukan tampil/tidak.

### Nilai Perusahaan
Mengatur kartu Integritas, Inovasi, Kemitraan, Keberlanjutan, atau menambah nilai baru.

## 4. Setelah menyimpan

Cukup refresh halaman:

```text
http://127.0.0.1:8000/
```

Tidak perlu mengubah `landing.html` setiap kali ingin mengganti konten.

## Catatan produksi

Upload gambar disimpan di `MEDIA_ROOT` (folder `media/`). Pada VPS production, arahkan Nginx ke folder media agar file upload dapat disajikan dengan cepat dan aman.
