import streamlit as st
from PIL import Image

from preprocessing import apply_scan_mode, adjust_brightness_contrast
from scanner import scan_document
from utils import cv2_to_pil, image_to_jpg_bytes, image_to_pdf_bytes, pil_to_cv2


st.set_page_config(
    page_title="Smart Document Scanner",
    layout="wide",
)


def main():
    st.title("Smart Document Scanner")

    st.sidebar.header("Pengaturan Scan")
    scan_mode = st.sidebar.selectbox(
        "Mode scan",
        ["Original", "Grayscale", "High Contrast", "Black & White"],
    )
    brightness = st.sidebar.slider("Brightness", -100, 100, 0)
    contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.2, 0.1)

    uploaded_file = st.file_uploader(
        "Upload gambar dokumen",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:
        st.info("Silakan upload gambar dokumen berformat JPG atau PNG.")
        return

    if st.session_state.get("uploaded_file_name") != uploaded_file.name:
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.scan_result = None

    original_pil = Image.open(uploaded_file).convert("RGB")
    original_cv = pil_to_cv2(original_pil)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Gambar Asli")
        st.image(original_pil, use_container_width=True)

    scan_button = st.button("Scan Document", type="primary")

    if "scan_result" not in st.session_state:
        st.session_state.scan_result = None

    if scan_button:
        with st.spinner("Memindai dokumen dan memperbaiki perspektif..."):
            scanned = scan_document(original_cv)
            enhanced = adjust_brightness_contrast(scanned, brightness, contrast)
            result = apply_scan_mode(enhanced, scan_mode)
            st.session_state.scan_result = result

    with right_col:
        st.subheader("Hasil Scan")
        if st.session_state.scan_result is None:
            st.warning("Klik tombol Scan Document untuk melihat hasil scan.")
        else:
            st.image(cv2_to_pil(st.session_state.scan_result), use_container_width=True)

            jpg_bytes = image_to_jpg_bytes(st.session_state.scan_result)
            pdf_bytes = image_to_pdf_bytes(st.session_state.scan_result)

            download_col_1, download_col_2 = st.columns(2)
            with download_col_1:
                st.download_button(
                    "Download Hasil (JPG)",
                    data=jpg_bytes,
                    file_name="hasil_scan.jpg",
                    mime="image/jpeg",
                )
            with download_col_2:
                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name="hasil_scan.pdf",
                    mime="application/pdf",
                )


if __name__ == "__main__":
    main()
