import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from functools import wraps
import requests
import json
from datetime import datetime
from werkzeug.exceptions import BadRequest
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

users = {}

# Fungsi untuk memeriksa API key yang valid
def is_valid_api_key(api_key):
    try:
        test_url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={api_key}"
        response = requests.get(test_url)
        return response.status_code == 200
    except:
        return False

# Decorator untuk memeriksa apakah pengguna telah login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Silakan login terlebih dahulu!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Fungsi untuk memvalidasi respons API (indikator keamanan)
def validate_weather_response(response):
    required_fields = ['coord', 'weather', 'main', 'wind', 'sys', 'name']
    
    for field in required_fields:
        if field not in response:
            return False
    
    if not isinstance(response['weather'], list) or len(response['weather']) == 0:
        return False
    
    return True

# Fungsi untuk mendapatkan data cuaca
def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        data = response.json()
        
        # Validasi respons
        if not validate_weather_response(data):
            raise ValueError("Invalid API response format")
        
        return data
    except requests.exceptions.RequestException as e:
        app.logger.error(f"API request error: {str(e)}")
        raise
    except ValueError as e:
        app.logger.error(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        raise

# Route untuk halaman beranda
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and bcrypt.check_password_hash(users[username]['password'], password):
            session['username'] = username
            session['api_key'] = users[username]['api_key']
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
    
    return render_template('login.html')

# Route untuk halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        api_key = request.form.get('api_key')
        
        if username in users:
            flash('Username sudah digunakan!', 'danger')
        elif not is_valid_api_key(api_key):
            flash('API key tidak valid!', 'danger')
        else:
            # Hash password sebelum disimpan
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            users[username] = {
                'password': hashed_password,
                'api_key': api_key
            }
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

# Route untuk dashboard cuaca
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        
        # Gunakan geocoding API untuk mendapatkan koordinat kota
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={session['api_key']}"
        
        try:
            geo_response = requests.get(geocoding_url)
            geo_data = geo_response.json()
            
            if geo_data and len(geo_data) > 0:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
                
                # Dapatkan data cuaca
                weather_data = get_weather_data(lat, lon, session['api_key'])
                
                # Format data untuk tampilan
                weather_data['main']['temp'] = round(weather_data['main']['temp'])
                weather_data['main']['feels_like'] = round(weather_data['main']['feels_like'])
                
                # Konversi timestamp Unix ke waktu yang mudah dibaca
                weather_data['sys']['sunrise_formatted'] = datetime.fromtimestamp(
                    weather_data['sys']['sunrise']).strftime('%H:%M')
                weather_data['sys']['sunset_formatted'] = datetime.fromtimestamp(
                    weather_data['sys']['sunset']).strftime('%H:%M')
                
                # Format tanggal dan waktu saat ini
                weather_data['current_time'] = datetime.now().strftime('%A, %d %B %Y, %H:%M')
                
            else:
                error = 'Kota tidak ditemukan!'
        
        except Exception as e:
            error = f'Terjadi kesalahan: {str(e)}'
    
    return render_template('dashboard.html', weather=weather_data, error=error)

# Route untuk logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('api_key', None)
    flash('Anda telah keluar dari sistem!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not app.config['SECRET_KEY']:
        app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    app.run(debug=True)