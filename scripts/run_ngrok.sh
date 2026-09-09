#!/bin/bash
set -e

if ! command -v ngrok >/dev/null 2>&1; then
  echo "ngrok belum terinstall. macOS: brew install ngrok"
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "Aktifkan virtualenv terlebih dahulu: source env/bin/activate"
  exit 1
fi

python manage.py runserver 127.0.0.1:8000 &
DJANGO_PID=$!
trap 'kill $DJANGO_PID 2>/dev/null || true' EXIT INT TERM

echo "Django berjalan di http://127.0.0.1:8000"
echo "Membuka tunnel ngrok..."
ngrok http 8000
