# 🌦️ WeatherApp — Aplikasi Cuaca dengan Flask & OpenWeatherAPI

WeatherApp adalah aplikasi web yang memungkinkan pengguna melihat informasi cuaca real-time berdasarkan nama kota. Aplikasi ini menggunakan **Flask**, **OpenWeatherAPI**, serta **Tailwind CSS** untuk antarmuka yang modern dan responsif. Aplikasi juga menerapkan praktik **keamanan autentikasi** dan **validasi API** yang baik.

---

## 🔧 Fitur Utama

### 🌐 Permintaan ke OpenWeatherAPI

- Aplikasi menggunakan pustaka `requests` untuk mengirim HTTP request ke **OpenWeatherAPI**.
- Implementasi utama berada di fungsi `get_weather_data()` pada `app.py`.
- Data cuaca diambil berdasarkan **koordinat latitude dan longitude** dari hasil pencarian nama kota.

### 🎨 Tampilan Web dengan Tailwind CSS

- Desain antarmuka menggunakan **Tailwind CSS via CDN**.
- Layout responsif dengan **sistem grid**.
- UI modern: kartu cuaca, indikator, dan form login/registrasi.

### 🔐 Mekanisme Autentikasi Aman

- Login dan registrasi menggunakan **bcrypt** untuk hashing password.
- **Manajemen sesi** menjaga informasi pengguna yang telah login.
- Validasi API key saat registrasi untuk memastikan keabsahan akses.
- Gunakan `login_required` decorator untuk membatasi akses ke rute privat.

### 🛡️ Validasi Respons API

- Fungsi `validate_weather_response()` memastikan respons dari API lengkap dan valid.
- Mencegah kesalahan data dan respons yang tidak sesuai ditampilkan ke pengguna.

---

## 🗂️ Struktur Proyek

├── app.py # File utama aplikasi Flask
├── config.py # Konfigurasi aplikasi (SECRET_KEY, API URL)
├── .env # Menyimpan variabel sensitif (API key, secret key)
├── requirements.txt # Daftar dependensi Python
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── dashboard.html
└── static/
└── js/
└── script.js # JavaScript untuk UI interaktif

## ⚙️ Cara Kerja Aplikasi

### 1. Registrasi dan Login

- Pengguna mendaftar menggunakan **username**, **password**, dan **API key** dari OpenWeather.
- Sistem memvalidasi API key sebelum menyimpan data.
- Setelah terdaftar, pengguna dapat login dan diarahkan ke dashboard.

### 2. Pencarian Cuaca

- Di dashboard, pengguna dapat mencari nama kota.
- Aplikasi menggunakan OpenWeather **Geocoding API** untuk mendapatkan koordinat kota.
- Cuaca ditampilkan berdasarkan koordinat tersebut secara interaktif.

### 3. Keamanan

- Password disimpan dalam bentuk **hash (bcrypt)**.
- API key hanya disimpan di **server-side session** dan tidak ditampilkan ke pengguna.
- Validasi semua data API untuk menghindari error & bug.
- Penanganan error yang menyeluruh untuk pengalaman pengguna yang aman.

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Instalasi Dependensi

```bash
pip install -r requirements.txt
```

### 2. Konfigurasi

Buat file .env di root proyek:

```bash
OPENWEATHER_API_KEY=masukkan_api_key_anda
SECRET_KEY=rahasia_anda
```

### 3. Menjalankan Aplikasi

jalankan program dengan perintah:

```bash
python app.py
```

### 4. Akses Aplikasi

Buka browser dan akses:

```bash
http://localhost:5000
```
