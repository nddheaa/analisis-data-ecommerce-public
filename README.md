
# E-Commerce Public Dataset 🌟

Selamat datang di proyek **E-Commerce Public Dataset**! 🎉 Proyek ini menggunakan dataset publik e-commerce untuk analisis data dan visualisasi interaktif menggunakan Streamlit. Berikut adalah panduan untuk menyiapkan dan menjalankan proyek ini di lingkungan Anda.

## 🚀 Setup Environment

### Anaconda

1. **Buat lingkungan baru**:
   ```bash
   conda create --name ecom-ds python=3.9
   ```

2. **Aktifkan lingkungan**:
   ```bash
   conda activate ecom-ds
   ```

3. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

### Shell/Terminal

1. **Buat folder proyek**:
   ```bash
   mkdir ecom-data-analysis
   cd ecom-data-analysis
   ```

2. **Instal `pipenv`** (jika belum terpasang):
   ```bash
   pip install pipenv
   ```

3. **Instal dependensi dan aktifkan virtual environment**:
   ```bash
   pipenv install
   pipenv shell
   ```

4. **Instal dependensi tambahan dari `requirements.txt`**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎬 Menjalankan Aplikasi Streamlit

Untuk menjalankan aplikasi Streamlit dan melihat dashboard analisis data, gunakan perintah berikut:

```bash
streamlit run dashboard.py
```

## 🛠️ Struktur Proyek

- `dashboard.py`: Skrip utama untuk aplikasi Streamlit.
- `requirements.txt`: Daftar paket Python yang diperlukan.
- `data/`: Folder berisi dataset CSV.

## 📄 Deskripsi

Proyek ini bertujuan untuk melakukan analisis data e-commerce dengan visualisasi interaktif. Anda dapat melihat distribusi kategori transaksi, kategori pembayaran, dan jumlah transaksi per minggu melalui aplikasi Streamlit ini.
