from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

import streamlit as st


LOGGER = logging.getLogger("smart_document_scanner")


def configure_logging() -> None:
    """Configure application logging once for Streamlit reruns."""
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    LOGGER.setLevel(logging.INFO)


def initialize_session_state() -> None:
    """Create all shared Streamlit session keys used by the application."""
    defaults: dict[str, Any] = {
        "show_edit_panel": False,
        "show_filter_panel": False,
        "scanner_result": None,
        "pipeline_stages": {},
        "processing_time": 0.0,
        "current_filter": "Original",
        "total_scan": 0,
        "source_image": None,
        "last_resolution": "Auto",
        "history": [],
        "exports_count": 0,
        "timeline_steps": [],
        "last_error": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_history_entry(
    file_name: str,
    mode_scan: str,
    file_size: str,
    resolution: str,
    processing_time: float,
) -> None:
    """Append one scan activity entry to the in-memory session history."""
    entry = {
        "Nama File": file_name,
        "Tanggal": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Mode Scan": mode_scan,
        "Ukuran Gambar": file_size,
        "Resolusi": resolution,
        "Processing Time": f"{processing_time:.2f}s",
    }
    st.session_state.history.insert(0, entry)
    st.session_state.history = st.session_state.history[:25]
    LOGGER.info("History entry added for %s with mode %s", file_name, mode_scan)


def format_file_size(size_bytes: int) -> str:
    """Convert a raw byte count into a readable file size string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"
