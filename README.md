# Padi Emas Nusantara
Starter Django untuk pengelolaan pengeluaran operasional, hasil panen, penjualan, dan dashboard laba.

## Instalasi Mac
```bash
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buka `http://127.0.0.1:8000/`.

Jika sebelumnya pernah menjalankan versi lama di browser dan login mendapat CSRF 403, hapus cookie/site data untuk `127.0.0.1` atau gunakan jendela Incognito sekali. Project ini juga sudah mengatur CSRF trusted origins untuk `127.0.0.1:8000` dan `localhost:8000`.

## Dummy Seed Data

Untuk mengisi database dengan data contoh:

```bash
python manage.py migrate
python manage.py seed_dummy
```

Akun development yang dibuat:

- Username: `admin`
- Password: `admin12345`

Data contoh dibuat agar dashboard menampilkan:

- Pengeluaran: Rp185.500.000
- Hasil panen: 42.500 Kg
- Penjualan: Rp297.500.000
- Laba: Rp112.000.000

Untuk menghapus data transaksi lalu membuat ulang data dummy:

```bash
python manage.py seed_dummy --clear
```

> Data seed hanya untuk development/testing lokal. Ganti atau hapus password demo sebelum deployment production.


## Akses dari Internet dengan ngrok

Project ini sudah disiapkan untuk development melalui ngrok. Django tetap berjalan di `127.0.0.1:8000`, sedangkan ngrok membuat URL HTTPS publik yang meneruskan trafik ke port tersebut. Django tetap menggunakan `ALLOWED_HOSTS` dan `CSRF_TRUSTED_ORIGINS` untuk validasi host/Origin.

### 1. Install ngrok di macOS

Dengan Homebrew:

```bash
brew install ngrok
```

Tambahkan authtoken dari akun ngrok:

```bash
ngrok config add-authtoken "TOKEN_ANDA"
```

### 2. Jalankan Django

Terminal 1:

```bash
source env/bin/activate
python manage.py runserver 127.0.0.1:8000
```

### 3. Jalankan ngrok

Terminal 2:

```bash
ngrok http 8000
```

ngrok akan menampilkan URL HTTPS, misalnya:

```text
https://contoh-1234.ngrok-free.app
```

### 4. Konfigurasi host yang lebih aman

Salin hanya hostname-nya (tanpa `https://`), lalu jalankan ulang Django:

```bash
export NGROK_DOMAIN=contoh-1234.ngrok-free.app
export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,contoh-1234.ngrok-free.app
python manage.py runserver 127.0.0.1:8000
```

Dengan `NGROK_DOMAIN`, project otomatis menambahkan `https://contoh-1234.ngrok-free.app` ke `CSRF_TRUSTED_ORIGINS`.

### Cara cepat untuk testing

Jika URL ngrok berubah setiap kali dijalankan, Anda dapat mengaktifkan wildcard khusus development:

```bash
export ALLOW_NGROK_WILDCARD=1
python manage.py runserver 127.0.0.1:8000
```

Kemudian di terminal lain:

```bash
ngrok http 8000
```

Wildcard ini menerima subdomain `*.ngrok-free.app` dan `*.ngrok.io`. Gunakan cara `NGROK_DOMAIN` untuk konfigurasi yang lebih ketat.

### Jika login terkena CSRF 403

Pastikan URL yang dibuka adalah URL HTTPS ngrok yang sama dengan domain yang dikonfigurasi. Jangan mencampur cookie dari URL ngrok lama; gunakan jendela Incognito jika perlu. Django 4.2 memeriksa Origin/Referer untuk request POST sehingga origin publik perlu dipercaya secara eksplisit.

> ngrok cocok untuk demo, testing, atau akses sementara. Untuk aplikasi produksi, sebaiknya deploy Django di VPS/server dengan domain sendiri, HTTPS, Gunicorn/Uvicorn, dan reverse proxy. Jangan membagikan akun/password demo ke publik.


## Perbaikan CSS / Static Files V13

V13 menambahkan WhiteNoise, `STATIC_ROOT`, dan konfigurasi static files yang lebih aman untuk akses lokal maupun ngrok. Setelah install dependency, jalankan:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py runserver 127.0.0.1:8000
```

Untuk ngrok:

```bash
ngrok http 8000
```

Pastikan `.env`/environment menggunakan `DJANGO_DEBUG=1` saat development.


## Ngrok

This development build accepts ngrok-free.app and ngrok.io hosts by default.
Run Django on 127.0.0.1:8000, then run `ngrok http 8000`. No per-session host edit is required.
For production, replace the wildcard ngrok hosts with your exact domain.

## Branding & PDF Reports

- Logo Padi Emas Nusantara menggunakan logo yang disediakan pengguna pada sidebar, halaman login, favicon, dan kop laporan PDF.
- Laporan PDF tersedia untuk Laporan Keuangan, Peredaran Bruto, Neraca Keuangan, Pajak, dan Laporan per Musim Tanam.
- PDF menggunakan kop Padi Emas Nusantara, ringkasan KPI, tabel rincian, footer, dan nomor halaman dengan gaya laporan manajerial yang konsisten dengan Smart Shrimp Farm.
- Dependensi PDF: `reportlab>=4.2,<5`.
# padi-emas-nusantara
