FROM python:3.11

WORKDIR /app

# Salin file dependency
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin backend (termasuk main.py dan routes/)
COPY ./backend /app

# Salin folder frontend (biarkan struktur `frontend/static` dan `frontend/templates` tetap ada)
COPY ./frontend /app/frontend

# Jalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
