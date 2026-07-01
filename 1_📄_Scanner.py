import time
from collections.abc import Callable
from typing import Any

import numpy as np
import streamlit as st

from src.download import image_to_jpg_bytes, image_to_pdf_bytes
from src.filters import apply_filter
from src.preprocessing import image_to_png_bytes, load_image_from_upload, png_bytes_to_image
from src.scanner_engine import apply_manual_edits, auto_enhance, scan_document
from src.state import LOGGER, add_history_entry, configure_logging, format_file_size, initialize_session_state
from src.ui import configure_page, empty_scanner_state, metric_card, progress_timeline, render_header, render_sidebar


configure_logging()
configure_page("Scanner | Smart Document Scanner")
render_sidebar()
render_header("Smart Document Scanner", "Professional Document Scanning Platform")
initialize_session_state()


def run_processing(label: str, callback: Callable[[], dict[str, Any]]) -> dict[str, Any] | None:
    """Run an OpenCV callback while showing spinner and progress feedback."""
    timeline = [
        "Uploading...",
        "Detecting Document...",
        "Finding Corners...",
        "Perspective Transform...",
        "Enhancing...",
        "Done",
    ]
    progress = st.progress(0, text=label)
    try:
        with st.spinner(label):
            for index, step in enumerate(timeline[:-1], start=1):
                st.session_state.timeline_steps = timeline[:index]
                progress.progress(index * 16, text=step)
                time.sleep(0.05)
            result = callback()
            st.session_state.timeline_steps = timeline
            progress.progress(100, text="Done")
            time.sleep(0.05)
        return result
    except Exception as exc:
        LOGGER.exception("Image processing failed")
        st.session_state.last_error = str(exc)
        st.error("Gambar gagal diproses. Pastikan file valid, jelas, dan tidak rusak.")
        return None
    finally:
        progress.empty()


def persist_result(
    result: dict[str, Any],
    file_name: str,
    file_size: str,
    mode_scan: str = "Original",
) -> None:
    """Persist processed image output and metadata into Streamlit session state."""
    final_image: np.ndarray = result["final"]
    st.session_state.scanner_result = image_to_png_bytes(final_image)
    st.session_state.pipeline_stages = {
        name: image_to_png_bytes(stage) for name, stage in result.get("stages", {}).items()
    }
    st.session_state.processing_time = result.get("elapsed", 0.0)
    st.session_state.current_filter = mode_scan
    st.session_state.total_scan += 1
    height, width = final_image.shape[:2]
    st.session_state.last_resolution = f"{width} × {height}"
    add_history_entry(file_name, mode_scan, file_size, st.session_state.last_resolution, st.session_state.processing_time)


st.markdown(
    """
    <div class="upload-shell">
        <div class="panel-title">Upload Document</div>
        <div class="soft-note">Drag & drop dokumen Anda di sini. Supported: JPG, PNG, JPEG.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "Drag & Drop Document",
    type=["jpg", "png", "jpeg"],
    label_visibility="collapsed",
)

source_image = None
file_name = "untitled-document"
file_size = "-"
if uploaded_file is not None:
    try:
        source_image = load_image_from_upload(uploaded_file)
        st.session_state.source_image = image_to_png_bytes(source_image)
        file_name = uploaded_file.name
        file_size = format_file_size(uploaded_file.size)
        st.session_state.timeline_steps = ["Uploading..."]
        st.session_state.last_resolution = f"{source_image.shape[1]} × {source_image.shape[0]}"
    except Exception as exc:
        LOGGER.exception("Failed to load uploaded image")
        st.session_state.last_error = str(exc)
        st.error("File tidak bisa dibaca sebagai gambar. Gunakan JPG, JPEG, atau PNG yang valid.")

st.write("")
progress_timeline(st.session_state.timeline_steps)
st.write("")

preview_left, preview_right = st.columns(2, gap="large")
with preview_left:
    st.markdown('<div class="image-frame"><div class="frame-title">📷 Original Image <span>Ready</span></div>', unsafe_allow_html=True)
    if source_image is not None:
        st.image(source_image, use_container_width=True)
    else:
        empty_scanner_state("Belum ada dokumen", "Upload gambar dokumen untuk memulai scan profesional.")
    st.markdown("</div>", unsafe_allow_html=True)

with preview_right:
    st.markdown('<div class="image-frame"><div class="frame-title">🛡 Scanned Result <span>Preview</span></div>', unsafe_allow_html=True)
    if st.session_state.scanner_result is not None:
        st.image(st.session_state.scanner_result, use_container_width=True)
    elif source_image is not None:
        st.image(source_image, use_container_width=True)
    else:
        empty_scanner_state("Hasil scan menunggu", "Preview hasil akan muncul setelah proses OpenCV selesai.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

action_cols = st.columns(4)
with action_cols[0]:
    if st.button("🔍 Scan Document", use_container_width=True):
        if source_image is None:
            st.toast("Upload dokumen terlebih dahulu.", icon="📄")
        else:
            result = run_processing(
                "Scanning document",
                lambda: scan_document(source_image, brightness=12, contrast=18, edge_threshold=75, sharpen=28),
            )
            if result is not None:
                persist_result(result, file_name, file_size, "Full Scan")
                st.toast("Scan document selesai.", icon="✅")
with action_cols[1]:
    if st.button("✨ Auto Enhance", use_container_width=True):
        base_image = source_image
        if base_image is None:
            st.toast("Upload dokumen terlebih dahulu.", icon="📄")
        else:
            result = run_processing("Applying enhancement", lambda: auto_enhance(base_image))
            if result is not None:
                persist_result(result, file_name, file_size, "Auto Enhance")
                st.toast("Auto Enhance selesai.", icon="✨")
with action_cols[2]:
    if st.button("✏ Edit", use_container_width=True):
        st.session_state.show_edit_panel = not st.session_state.show_edit_panel
        st.toast("Edit panel dibuka.", icon="✏")
with action_cols[3]:
    if st.button("🎨 Filter", use_container_width=True):
        st.session_state.show_filter_panel = not st.session_state.show_filter_panel
        st.toast("Filter panel dibuka.", icon="🎨")

panel_left, panel_right = st.columns(2, gap="large")
if st.session_state.show_edit_panel:
    with panel_left:
        st.markdown(
            """
            <div class="glass-card">
                <div class="panel-title">✏ Edit</div>
                <div class="soft-note">Kontrol visual untuk tahap image adjustment berikutnya.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        brightness = st.slider("Brightness", -100, 100, 12)
        contrast = st.slider("Contrast", -100, 100, 18)
        edge_detection = st.slider("Edge Detection", 0, 100, 35)
        sharpen = st.slider("Sharpen", 0, 100, 20)
        rotate = st.selectbox("Rotate", ["90°", "180°", "270°"])
        edit_apply, edit_reset = st.columns(2)
        with edit_apply:
            if st.button("Apply", use_container_width=True):
                if source_image is None:
                    st.toast("Upload dokumen terlebih dahulu.", icon="📄")
                else:
                    result = run_processing(
                        "Applying edits",
                        lambda: apply_manual_edits(source_image, brightness, contrast, edge_detection, sharpen, rotate),
                    )
                    if result is not None:
                        persist_result(result, file_name, file_size, "Manual Edit")
                        st.toast("Edit settings diterapkan.", icon="✅")
        with edit_reset:
            if st.button("Reset", use_container_width=True):
                if source_image is not None:
                    st.session_state.scanner_result = image_to_png_bytes(source_image)
                    st.session_state.current_filter = "Original"
                    st.session_state.last_resolution = f"{source_image.shape[1]} × {source_image.shape[0]}"
                st.toast("Edit settings direset.", icon="↩")

if st.session_state.show_filter_panel:
    with panel_right:
        st.markdown(
            """
            <div class="glass-card">
                <div class="panel-title">🎨 Filter</div>
                <div class="soft-note">Pilih gaya pemrosesan visual untuk hasil scan.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        selected_filter = st.radio(
            "Choose Filter",
            ["Original", "Grayscale", "High Contrast", "Black & White", "Sepia", "Color Boost", "Document Boost"],
            label_visibility="collapsed",
        )
        if st.button("Apply Filter", use_container_width=True):
            if source_image is None:
                st.toast("Upload dokumen terlebih dahulu.", icon="📄")
            else:
                result = run_processing(
                    "Applying filter",
                    lambda: (lambda filtered_image: {
                        "elapsed": 0.0,
                        "stages": {"Original": source_image, "Final Scan": filtered_image},
                        "final": filtered_image,
                    })(apply_filter(source_image, selected_filter)),
                )
                if result is not None:
                    persist_result(result, file_name, file_size, selected_filter)
                    st.toast(f"Filter {selected_filter} diterapkan.", icon="✨")

if st.session_state.scanner_result is not None:
    result_image = png_bytes_to_image(st.session_state.scanner_result)
    download_cols = st.columns(2)
    with download_cols[0]:
        if st.download_button(
            "⬇ Download JPG",
            data=image_to_jpg_bytes(result_image),
            file_name="smart_document_scan.jpg",
            mime="image/jpeg",
            use_container_width=True,
        ):
            st.session_state.exports_count += 1
    with download_cols[1]:
        if st.download_button(
            "⬇ Download PDF",
            data=image_to_pdf_bytes(result_image),
            file_name="smart_document_scan.pdf",
            mime="application/pdf",
            use_container_width=True,
        ):
            st.session_state.exports_count += 1

st.write("")
st.markdown('<div class="glass-card"><div class="panel-title">Statistics</div></div>', unsafe_allow_html=True)
stat_cols = st.columns(4)
with stat_cols[0]:
    metric_card("Total Scan", str(st.session_state.total_scan), "Current session")
with stat_cols[1]:
    metric_card("Processing Time", f"{st.session_state.processing_time:.2f}s", "OpenCV runtime")
with stat_cols[2]:
    metric_card("Resolution", st.session_state.last_resolution, "Shown after processing")
with stat_cols[3]:
    metric_card("Current Filter", st.session_state.current_filter, "Active result")
