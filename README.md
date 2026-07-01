# Smart Document Scanner

Aplikasi web sederhana berbasis Streamlit untuk memindai dokumen dari gambar, meluruskan perspektif, meningkatkan kualitas gambar, lalu mengunduh hasil sebagai JPG atau PDF.

## Fitur

- Upload gambar dokumen JPG, JPEG, atau PNG.
- Deteksi tepi dokumen menggunakan OpenCV.
- Perspective transform untuk meluruskan dokumen.
- Mode scan: Original, Grayscale, High Contrast, dan Black & White.
- Pengaturan brightness dan contrast dari sidebar.
- Download hasil scan dalam format JPG dan PDF.

## Instalasi

```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

```bash
streamlit run app.py
```

## Struktur File

- `app.py`: antarmuka Streamlit.
- `scanner.py`: deteksi kontur dokumen dan perspective transform.
- `preprocessing.py`: brightness, contrast, grayscale, threshold, dan enhancement.
- `utils.py`: helper konversi gambar dan export file.
- `requirements.txt`: daftar dependency Python.
