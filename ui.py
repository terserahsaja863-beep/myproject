import html

import streamlit as st


MENU_ITEMS = [
    ("🏠", "Dashboard", "app.py", "/"),
    ("📄", "Scanner", "pages/1_📄_Scanner.py", "/Scanner"),
    ("🧪", "Image Processing", "pages/2_🧪_Image_Processing.py", "/Image_Processing"),
    ("🕒", "History", "pages/3_🕒_History.py", "/History"),
    ("ℹ", "About", "pages/4_ℹ_About.py", "/About"),
]


def configure_page(page_title: str = "Smart Document Scanner") -> None:
    """Configure the shared Streamlit page settings."""
    st.set_page_config(
        page_title=page_title,
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()


def inject_css() -> None:
    """Inject the shared custom CSS for the modern scanner interface."""
    st.markdown(
        """
        <style>
            :root {
                --primary: #2563EB;
                --secondary: #3B82F6;
                --bg: #F5F8FF;
                --card: #FFFFFF;
                --ink: #0F172A;
                --muted: #64748B;
                --line: #E2E8F0;
                --soft-shadow: 0 24px 60px rgba(15, 23, 42, 0.10);
                --small-shadow: 0 12px 28px rgba(37, 99, 235, 0.16);
                --radius: 20px;
            }

            * {
                letter-spacing: 0;
            }

            .stApp {
                background:
                    linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(245, 248, 255, 0.95) 34%, rgba(255, 255, 255, 1) 100%),
                    linear-gradient(180deg, #F5F8FF 0%, #FFFFFF 100%);
                color: var(--ink);
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            [data-testid="stSidebar"] {
                background:
                    linear-gradient(180deg, rgba(7, 18, 36, 0.98) 0%, rgba(15, 31, 61, 0.96) 56%, rgba(16, 43, 88, 0.98) 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.10);
                box-shadow: 24px 0 60px rgba(15, 23, 42, 0.12);
            }

            [data-testid="stSidebarNav"],
            [data-testid="stSidebarHeader"] {
                display: none;
            }

            [data-testid="stSidebar"] * {
                color: #F8FAFC;
            }

            .block-container {
                padding-top: 1.75rem;
                padding-bottom: 3rem;
                max-width: 1400px;
            }

            h1, h2, h3 {
                letter-spacing: 0;
                color: var(--ink);
            }

            .brand-shell {
                display: flex;
                gap: 0.9rem;
                align-items: center;
                padding: 1rem 0.25rem 1.25rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.09);
                margin-bottom: 0.65rem;
            }

            .brand-logo {
                width: 3rem;
                height: 3rem;
                display: grid;
                place-items: center;
                border-radius: 16px;
                background: linear-gradient(135deg, #2563EB, #22D3EE);
                box-shadow: 0 14px 28px rgba(34, 211, 238, 0.18);
                font-size: 1.45rem;
                transition: transform 180ms ease, box-shadow 180ms ease;
            }

            .brand-logo:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 18px 38px rgba(34, 211, 238, 0.28);
            }

            .brand-title {
                font-size: 1.08rem;
                font-weight: 800;
                line-height: 1.15;
            }

            .brand-subtitle {
                font-size: 0.82rem;
                color: rgba(226, 232, 240, 0.78) !important;
                margin-top: 0.15rem;
            }

            .sidebar-version {
                margin-top: 1.5rem;
                padding: 1rem;
                border-radius: 18px;
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.24), rgba(20, 184, 166, 0.16));
                border: 1px solid rgba(255, 255, 255, 0.14);
                color: rgba(226, 232, 240, 0.78) !important;
                font-size: 0.84rem;
                backdrop-filter: blur(18px);
            }

            [data-testid="stSidebar"] [data-testid="stPageLink"] a {
                border-radius: 15px;
                padding: 0.75rem 0.9rem;
                color: #E2E8F0;
                transition: all 180ms ease;
            }

            [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
                background: rgba(255, 255, 255, 0.12);
                transform: translateX(4px);
            }

            .fallback-page-link {
                display: block;
                border-radius: 15px;
                padding: 0.75rem 0.9rem;
                color: #E2E8F0 !important;
                text-decoration: none !important;
                margin-bottom: 0.15rem;
                transition: all 180ms ease;
            }

            .fallback-page-link:hover {
                background: rgba(255, 255, 255, 0.10);
                transform: translateX(4px);
            }

            .hero-header {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 1.4rem;
            }

            .eyebrow {
                color: var(--primary);
                font-size: 0.83rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.25rem;
            }

            .page-title {
                font-size: clamp(2rem, 4vw, 3.2rem);
                font-weight: 900;
                line-height: 1;
                margin: 0;
            }

            .page-subtitle {
                color: var(--muted);
                font-size: 1.02rem;
                margin-top: 0.65rem;
                max-width: 44rem;
            }

            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.58rem 0.85rem;
                border-radius: 999px;
                background: #ECFDF5;
                color: #047857;
                font-weight: 800;
                box-shadow: 0 10px 24px rgba(4, 120, 87, 0.09);
                white-space: nowrap;
                border: 1px solid rgba(16, 185, 129, 0.22);
            }

            .glass-card {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(255, 255, 255, 0.86);
                border-radius: var(--radius);
                padding: 1.25rem;
                box-shadow: var(--soft-shadow);
                backdrop-filter: blur(18px);
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }

            .glass-card:hover,
            .metric-card:hover,
            .feature-card:hover,
            .image-frame:hover {
                transform: translateY(-2px);
                box-shadow: 0 30px 70px rgba(15, 23, 42, 0.12);
                border-color: rgba(37, 99, 235, 0.20);
            }

            .metric-card {
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(255, 255, 255, 0.92);
                border-radius: var(--radius);
                padding: 1.15rem;
                min-height: 7rem;
                box-shadow: var(--soft-shadow);
                backdrop-filter: blur(16px);
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }

            .metric-label {
                color: var(--muted);
                font-size: 0.82rem;
                font-weight: 700;
                margin-bottom: 0.45rem;
            }

            .metric-value {
                color: var(--ink);
                font-size: 1.55rem;
                font-weight: 900;
            }

            .metric-hint {
                color: var(--muted);
                font-size: 0.8rem;
                margin-top: 0.25rem;
            }

            .upload-shell {
                border: 1.5px dashed rgba(37, 99, 235, 0.36);
                border-radius: var(--radius);
                background: rgba(255, 255, 255, 0.68);
                padding: 1.35rem;
                box-shadow: 0 12px 34px rgba(37, 99, 235, 0.07);
                backdrop-filter: blur(18px);
                transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
            }

            .upload-shell:hover {
                border-color: rgba(37, 99, 235, 0.62);
                box-shadow: 0 24px 58px rgba(37, 99, 235, 0.13);
                transform: translateY(-1px);
            }

            .image-frame {
                background: rgba(255, 255, 255, 0.84);
                border: 1px solid rgba(255, 255, 255, 0.94);
                border-radius: var(--radius);
                padding: 1rem;
                box-shadow: var(--soft-shadow);
                backdrop-filter: blur(16px);
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }

            .frame-title {
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-weight: 850;
                margin-bottom: 0.85rem;
                color: var(--ink);
            }

            .placeholder {
                min-height: 26rem;
                border-radius: 16px;
                border: 1px dashed rgba(148, 163, 184, 0.58);
                background:
                    linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(255, 255, 255, 0.5)),
                    repeating-linear-gradient(45deg, rgba(148, 163, 184, 0.08) 0, rgba(148, 163, 184, 0.08) 10px, transparent 10px, transparent 20px);
                display: grid;
                place-items: center;
                text-align: center;
                color: var(--muted);
                padding: 1rem;
            }

            .empty-state {
                min-height: 26rem;
                border-radius: 18px;
                border: 1px dashed rgba(37, 99, 235, 0.28);
                background: linear-gradient(145deg, rgba(239, 246, 255, 0.86), rgba(255, 255, 255, 0.76));
                display: grid;
                place-items: center;
                text-align: center;
                padding: 1.5rem;
                color: var(--muted);
            }

            .scanner-illustration {
                width: min(13rem, 74%);
                margin: 0 auto 1rem;
                aspect-ratio: 1.15;
                border-radius: 28px;
                background:
                    linear-gradient(135deg, rgba(37, 99, 235, 0.16), rgba(20, 184, 166, 0.12)),
                    #FFFFFF;
                box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.12), 0 18px 44px rgba(37, 99, 235, 0.12);
                position: relative;
            }

            .scanner-illustration::before {
                content: "";
                position: absolute;
                left: 18%;
                right: 18%;
                top: 16%;
                height: 56%;
                border-radius: 12px;
                background: #FFFFFF;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.10);
            }

            .scanner-illustration::after {
                content: "";
                position: absolute;
                left: 14%;
                right: 14%;
                bottom: 18%;
                height: 18%;
                border-radius: 999px;
                background: linear-gradient(90deg, #2563EB, #14B8A6);
                box-shadow: 0 12px 30px rgba(37, 99, 235, 0.22);
            }

            .placeholder strong {
                display: block;
                color: var(--ink);
                font-size: 1.05rem;
                margin-bottom: 0.25rem;
            }

            .stButton > button,
            .stDownloadButton > button {
                border-radius: 16px;
                border: 1px solid rgba(37, 99, 235, 0.18);
                padding: 0.72rem 1rem;
                font-weight: 800;
                background: #FFFFFF;
                color: var(--ink);
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
                transition: all 180ms ease;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover {
                border-color: rgba(37, 99, 235, 0.42);
                color: var(--primary);
                transform: translateY(-1px);
                box-shadow: 0 14px 30px rgba(37, 99, 235, 0.15);
            }

            div[data-testid="stHorizontalBlock"] .stButton:first-child > button {
                background: linear-gradient(135deg, var(--primary), #14B8A6);
                color: white;
                border: none;
                box-shadow: var(--small-shadow);
            }

            .timeline {
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 0.7rem;
                margin: 1rem 0 0.4rem;
            }

            .timeline-step {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid rgba(226, 232, 240, 0.90);
                border-radius: 16px;
                padding: 0.8rem 0.65rem;
                text-align: center;
                color: var(--muted);
                font-size: 0.8rem;
                font-weight: 800;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
                transition: all 180ms ease;
            }

            .timeline-step.done {
                color: #075985;
                border-color: rgba(37, 99, 235, 0.28);
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(20, 184, 166, 0.10));
            }

            .timeline-dot {
                display: block;
                width: 0.65rem;
                height: 0.65rem;
                margin: 0 auto 0.4rem;
                border-radius: 999px;
                background: #CBD5E1;
            }

            .timeline-step.done .timeline-dot {
                background: linear-gradient(135deg, #2563EB, #14B8A6);
                box-shadow: 0 0 0 5px rgba(37, 99, 235, 0.10);
            }

            .panel-title {
                font-size: 1.15rem;
                font-weight: 900;
                margin-bottom: 0.25rem;
            }

            .soft-note {
                color: var(--muted);
                font-size: 0.92rem;
            }

            .filter-pill {
                padding: 0.8rem 0.95rem;
                border-radius: 16px;
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                color: var(--ink);
                font-weight: 760;
                margin-bottom: 0.55rem;
                transition: all 180ms ease;
            }

            .filter-pill:hover {
                transform: translateX(3px);
                border-color: rgba(37, 99, 235, 0.25);
            }

            .feature-row {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 1rem;
            }

            .feature-card {
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(255, 255, 255, 0.92);
                border-radius: var(--radius);
                padding: 1.05rem;
                box-shadow: var(--soft-shadow);
                min-height: 9.5rem;
                backdrop-filter: blur(16px);
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }

            .feature-icon {
                width: 2.6rem;
                height: 2.6rem;
                display: grid;
                place-items: center;
                border-radius: 15px;
                background: #EFF6FF;
                color: var(--primary);
                font-size: 1.25rem;
                margin-bottom: 0.8rem;
            }

            [data-testid="stFileUploader"] {
                background: transparent;
            }

            [data-testid="stFileUploader"] section {
                border: 0;
                background: transparent;
                padding: 0;
            }

            [data-testid="stFileUploader"] button {
                border-radius: 14px;
                background: linear-gradient(135deg, var(--primary), #7C3AED);
                color: #FFFFFF;
                border: none;
            }

            [data-testid="stMetricValue"] {
                color: var(--ink);
            }

            @media (max-width: 900px) {
                .hero-header {
                    flex-direction: column;
                }

                .feature-row {
                    grid-template-columns: 1fr;
                }

                .placeholder,
                .empty-state {
                    min-height: 17rem;
                }

                .timeline {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render the custom sidebar with brand, menu, and version information."""
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-shell">
                <div class="brand-logo">📄</div>
                <div>
                    <div class="brand-title">Smart Document Scanner</div>
                    <div class="brand-subtitle">Powered by OpenCV</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for icon, label, target, url in MENU_ITEMS:
            try:
                st.page_link(target, label=f"{icon}  {label}")
            except Exception:
                st.markdown(
                    f'<a class="fallback-page-link" href="{url}" target="_self">{icon}  {label}</a>',
                    unsafe_allow_html=True,
                )
        st.markdown(
            """
            <div class="sidebar-version">
                <strong>Version 1.0</strong><br>
                Premium OpenCV document scanner.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_header(title: str = "Smart Document Scanner", subtitle: str = "Professional Document Scanning Platform") -> None:
    """Render a reusable page header with online status badge."""
    st.markdown(
        f"""
        <div class="hero-header">
            <div>
                <div class="eyebrow">Document Intelligence</div>
                <h1 class="page-title">{title}</h1>
                <div class="page-subtitle">{subtitle}</div>
            </div>
            <div class="status-badge">🟢 Online</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, hint: str = "") -> None:
    """Render a compact statistics card with label, value, and helper text."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(icon: str, title: str, body: str) -> None:
    """Render a reusable feature card for dashboard and about pages."""
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p class="soft-note">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_scanner_state(title: str, body: str) -> None:
    """Render a polished empty state with a pure-CSS scanner illustration."""
    st.markdown(
        f"""
        <div class="empty-state">
            <div>
                <div class="scanner-illustration"></div>
                <strong>{html.escape(title)}</strong>
                <div>{html.escape(body)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def progress_timeline(completed_steps: list[str]) -> None:
    """Render the scan progress timeline with completed states."""
    steps = [
        "Uploading...",
        "Detecting Document...",
        "Finding Corners...",
        "Perspective Transform...",
        "Enhancing...",
        "Done",
    ]
    items = []
    completed = set(completed_steps)
    for step in steps:
        class_name = "timeline-step done" if step in completed else "timeline-step"
        items.append(f'<div class="{class_name}"><span class="timeline-dot"></span>{html.escape(step)}</div>')
    st.markdown(f'<div class="timeline">{"".join(items)}</div>', unsafe_allow_html=True)
