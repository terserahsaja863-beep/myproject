# Smart Document Scanner

Smart Document Scanner adalah aplikasi pemindai dokumen berbasis **Python**, **Streamlit**, dan **OpenCV**. Project ini dibuat dengan UI modern, pipeline image processing modular, fitur download JPG/PDF, history sesi, dan halaman visualisasi tahapan pemrosesan.

## Fitur

- Upload dokumen JPG, JPEG, dan PNG
- Scan dokumen dengan pipeline OpenCV
- Auto Enhance untuk brightness, contrast, histogram equalization, dan sharpen
- Edit manual: brightness, contrast, edge detection, sharpen, rotate
- Filter: Original, Grayscale, High Contrast, Black & White, Sepia, Color Boost, Document Boost
- Progress timeline proses scan
- Empty state modern sebelum upload
- History scan dalam session state
- Download hasil sebagai JPG dan PDF
- Halaman Image Processing dengan grid tahapan dan histogram before/after

## Teknologi

- **Python**: bahasa utama aplikasi
- **Streamlit**: framework frontend dan multipage app
- **OpenCV**: image processing dan document scanning pipeline
- **NumPy**: operasi array gambar
- **Pillow**: membaca dan mengubah format gambar
- **Matplotlib**: visualisasi histogram
- **ReportLab**: export hasil scan ke PDF

## Struktur Project

```text
.
├── app.py
├── requirements.txt
├── README.md
├── pages/
│   ├── 1_📄_Scanner.py
│   ├── 2_🧪_Image_Processing.py
│   ├── 3_🕒_History.py
│   └── 4_ℹ_About.py
└── src/
    ├── download.py
    ├── filters.py
    ├── geometry.py
    ├── histogram.py
    ├── preprocessing.py
    ├── scanner_engine.py
    ├── state.py
    └── ui.py
```

## Instalasi

Pastikan Python 3.10 atau lebih baru sudah terpasang.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Untuk macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cara Menjalankan

```bash
streamlit run app.py
```

Setelah server aktif, buka URL lokal yang ditampilkan oleh Streamlit, biasanya:

```text
http://localhost:8501
```

## Cara Deploy ke Streamlit Community Cloud

1. Upload project ini ke repository GitHub.
2. Pastikan file `requirements.txt` berada di root project.
3. Buka [Streamlit Community Cloud](https://streamlit.io/cloud).
4. Pilih **New app**.
5. Hubungkan repository GitHub.
6. Isi main file path:

```text
app.py
```

7. Klik **Deploy**.

## Catatan Pengembangan

- History disimpan di `st.session_state`, sehingga akan hilang ketika session berakhir.
- Aplikasi memakai `opencv-python-headless` agar cocok untuk cloud deployment.
- Kode dibuat modular agar mudah dipahami, dipresentasikan, dan dikembangkan.
