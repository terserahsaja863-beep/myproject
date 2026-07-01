import streamlit as st

from src.state import configure_logging, initialize_session_state
from src.ui import configure_page, info_card, metric_card, render_header, render_sidebar


configure_logging()
configure_page("Dashboard | Smart Document Scanner")
render_sidebar()
initialize_session_state()
render_header()

history_count = len(st.session_state.history)
latest_item = st.session_state.history[0] if st.session_state.history else None

stats = st.columns(4)
with stats[0]:
    metric_card("Total Scan", str(st.session_state.total_scan), "Current session")
with stats[1]:
    metric_card("Processing Time", f"{st.session_state.processing_time:.2f}s", "Last OpenCV process")
with stats[2]:
    metric_card("Resolution", st.session_state.last_resolution, "Latest result")
with stats[3]:
    metric_card("Current Filter", st.session_state.current_filter, "Active mode")

st.write("")

left, right = st.columns([1.35, 0.85], gap="large")
with left:
    st.markdown(
        """
        <div class="glass-card">
            <div class="panel-title">Workspace Overview</div>
            <div class="soft-note">
                Kelola alur scan dokumen dengan tampilan SaaS modern. Aplikasi ini sudah
                terhubung ke pipeline OpenCV untuk scan, enhancement, filter, export, dan history.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        info_card("📄", "Scanner Ready", "Upload JPG, PNG, atau JPEG dan proses dokumen dengan pipeline OpenCV.")
    with cols[1]:
        info_card("✨", "Enhancement Tools", "Brightness, contrast, edge detection, sharpen, rotate, dan filter bekerja real-time.")
    with cols[2]:
        info_card("☁", "Cloud Friendly", "Siap diunggah ke GitHub dan dideploy ke Streamlit Community Cloud.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown(
            """
            <div class="glass-card">
                <div class="panel-title">Recent Activity</div>
                <p class="soft-note">Ringkasan aktivitas pemrosesan pada sesi ini.</p>
                <div class="filter-pill">🟢 Scanner interface online</div>
                <div class="filter-pill">🧪 OpenCV pipeline ready</div>
                <div class="filter-pill">🕒 {history_count} history item(s)</div>
                <div class="filter-pill">📄 Latest: {latest}</div>
            </div>
        """.format(history_count=history_count, latest=latest_item["Nama File"] if latest_item else "No scan yet"),
        unsafe_allow_html=True,
    )
