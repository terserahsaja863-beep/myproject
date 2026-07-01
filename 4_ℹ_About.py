import streamlit as st

from src.state import configure_logging, initialize_session_state
from src.ui import configure_page, info_card, render_header, render_sidebar


configure_logging()
configure_page("About | Smart Document Scanner")
render_sidebar()
initialize_session_state()
render_header("About", "Technology stack and project overview")

st.markdown(
    """
    <div class="glass-card">
        <div class="panel-title">Smart Document Scanner</div>
        <div class="soft-note">
            Smart Document Scanner adalah aplikasi pemindai dokumen berbasis Streamlit yang
            menggabungkan UI premium dengan pipeline OpenCV. Project ini dibuat modular agar mudah
            dipelajari, dipresentasikan, dan dikembangkan oleh mahasiswa.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(3)
with cols[0]:
    info_card("🐍", "Python", "Bahasa utama untuk menghubungkan UI, proses gambar, session state, dan export dokumen.")
with cols[1]:
    info_card("👁", "OpenCV", "Digunakan untuk grayscale, blur, edge detection, contour, transform perspektif, threshold, dan sharpening.")
with cols[2]:
    info_card("🔢", "NumPy", "Representasi array gambar dan operasi numerik yang efisien selama pipeline scanner berjalan.")

cols = st.columns(3)
with cols[0]:
    info_card("🖼", "Pillow", "Membaca upload gambar, mengubah format, dan menyiapkan data gambar untuk download.")
with cols[1]:
    info_card("📊", "Matplotlib", "Membuat Histogram Before dan Histogram After pada halaman Image Processing.")
with cols[2]:
    info_card("⚡", "Streamlit", "Framework UI multipage yang ringan, cepat dibuat, dan siap deploy ke Community Cloud.")

st.write("")
st.markdown(
    """
    <div class="glass-card">
        <div class="panel-title">Project Highlights</div>
        <div class="filter-pill">✅ Modular code structure for learning and maintenance</div>
        <div class="filter-pill">✅ OpenCV backend connected to all scanner actions</div>
        <div class="filter-pill">✅ JPG/PDF export and session-based history</div>
        <div class="filter-pill">✅ Ready for GitHub and Streamlit Community Cloud</div>
    </div>
    """,
    unsafe_allow_html=True,
)
