import os
from datetime import timedelta

class Config:
    # Konfigurasi umum
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-jangan-gunakan-di-produksi'
    
    # Konfigurasi sesi
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # OpenWeather API key default (untuk development)
    # Dalam produksi, gunakan environment variable
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    
    # Batas permintaan API per pengguna per hari
    # Ini akan diimplementasikan di aplikasi
    API_REQUEST_LIMIT = 50