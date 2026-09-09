Padi Emas Nusantara — Landing Page Update

Perubahan utama:
- Beranda / sekarang menjadi landing page company profile.
- Login tetap tersedia di /login/.
- Dashboard aplikasi dipindahkan ke /dashboard/.
- Semua menu aplikasi tetap memakai URL yang sudah ada.
- Tombol "Masuk Aplikasi" pada landing page menuju /login/.
- Logo Padi Emas Nusantara diganti menggunakan logo yang diberikan.
- Favicon/app icon diperbarui dari logo tersebut.
- Landing page responsif desktop/tablet/mobile.
- Tersedia section Tentang Kami, Kegiatan, Fasilitas, Galeri, Keunggulan, CTA aplikasi, dan Kontak.
- Dashboard tetap mempertahankan fitur DOC dan prediksi Open-Meteo 5 hari.

Setelah ekstrak:
python manage.py migrate
python manage.py collectstatic --noinput   # opsional untuk deployment
python manage.py runserver 0.0.0.0:8000
