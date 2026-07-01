import streamlit as st

from src.histogram import create_histogram_figure
from src.preprocessing import image_to_png_bytes, load_image_from_upload, png_bytes_to_image
from src.scanner_engine import scan_document
from src.state import LOGGER, configure_logging, initialize_session_state
from src.ui import configure_page, render_header, render_sidebar


configure_logging()
configure_page("Image Processing | Smart Document Scanner")
render_sidebar()
initialize_session_state()
render_header("Image Processing", "OpenCV pipeline stages for document scanning")

st.markdown(
    """
    <div class="glass-card">
        <div class="panel-title">Processing Pipeline</div>
        <div class="soft-note">
            Setiap tahap pemrosesan dokumen ditampilkan dalam grid agar alur OpenCV mudah diperiksa.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload image for pipeline preview",
    type=["jpg", "png", "jpeg"],
    label_visibility="collapsed",
)

source_image = None
if uploaded_file is not None:
    try:
        source_image = load_image_from_upload(uploaded_file)
        st.session_state.source_image = image_to_png_bytes(source_image)
        if st.session_state.get("image_processing_upload_name") != uploaded_file.name:
            st.session_state.pipeline_stages = {}
            st.session_state.image_processing_upload_name = uploaded_file.name
    except Exception as exc:
        LOGGER.exception("Failed to load image on Image Processing page")
        st.session_state.last_error = str(exc)
        st.error("File tidak bisa dibaca sebagai gambar. Gunakan JPG, JPEG, atau PNG yang valid.")
        st.stop()
elif st.session_state.get("source_image") is not None:
    source_image = png_bytes_to_image(st.session_state.source_image)

if source_image is None:
    st.info("Upload dokumen di halaman ini atau proses gambar dari halaman Scanner terlebih dahulu.")
    st.stop()

if st.button("Refresh Pipeline", use_container_width=True):
    st.session_state.pipeline_stages = {}

stage_order = [
    "Original",
    "Grayscale",
    "Gaussian Blur",
    "Edge Detection",
    "Contour Detection",
    "Perspective Transform",
    "Threshold",
    "Histogram Equalization",
    "Final Scan",
]

missing_required_stage = any(name not in st.session_state.get("pipeline_stages", {}) for name in stage_order)
if not st.session_state.get("pipeline_stages") or missing_required_stage:
    with st.spinner("Generating OpenCV stages"):
        try:
            result = scan_document(source_image)
            st.session_state.pipeline_stages = {
                name: image_to_png_bytes(stage) for name, stage in result["stages"].items()
            }
            st.session_state.scanner_result = image_to_png_bytes(result["final"])
            st.session_state.processing_time = result["elapsed"]
        except Exception as exc:
            LOGGER.exception("Pipeline generation failed")
            st.session_state.last_error = str(exc)
            st.error("Pipeline gagal dibuat. Coba gunakan gambar dokumen yang lebih jelas.")
            st.stop()

st.write("")
grid = st.columns(3)
for index, title in enumerate(stage_order):
    image_bytes = st.session_state.pipeline_stages.get(title)
    if image_bytes is None:
        continue
    with grid[index % 3]:
        st.markdown(
            f"""
            <div class="image-frame">
                <div class="frame-title">{title}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.image(image_bytes, use_container_width=True)

before = png_bytes_to_image(st.session_state.pipeline_stages["Original"])
after = png_bytes_to_image(st.session_state.pipeline_stages["Final Scan"])
st.write("")
st.markdown('<div class="glass-card"><div class="panel-title">Histogram Before & After</div></div>', unsafe_allow_html=True)
st.pyplot(create_histogram_figure(before, after), use_container_width=True)
