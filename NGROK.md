# Quick ngrok

```bash
source env/bin/activate
python manage.py runserver 127.0.0.1:8000
```

Terminal lain:

```bash
ngrok http 8000
```

Untuk URL yang berubah-ubah, development cepat:

```bash
export ALLOW_NGROK_WILDCARD=1
python manage.py runserver 127.0.0.1:8000
```

Untuk keamanan lebih baik, set `NGROK_DOMAIN` ke hostname ngrok yang sedang aktif.
