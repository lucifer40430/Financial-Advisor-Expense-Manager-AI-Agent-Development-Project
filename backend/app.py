import sys
import tempfile
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

# Existing backend functions — intentionally unchanged.
from backend.ocr.vision_ocr import vision_transcribe
from backend.expense.expense_parser import parse_expense
from backend.database.expense_db import save_expense
from backend.ai.financial_advisor import get_financial_advice
from backend.dashboard import show_dashboard


# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="FinSight AI | Personal Finance Intelligence",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded",
)

USER_ID = 1


# ============================================================
# THEME STATE
# ============================================================
# Always start the application in dark mode
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

CURRENT_THEME = st.session_state.theme


# ============================================================
# THEME / CSS
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --fs-primary: #635bff;
        --fs-primary-dark: #5147e8;
        --fs-green: #16a34a;
        --fs-text: #111827;
        --fs-muted: #6b7280;
        --fs-border: rgba(100, 116, 139, 0.18);
        --fs-soft: rgba(99, 91, 255, 0.07);
    }

    /* Global layout */
    .block-container {
        max-width: 1450px;
        padding-top: 1.2rem;
        padding-bottom: 6rem;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid var(--fs-border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.1rem;
        padding-bottom: 1.5rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: .65rem;
        margin-bottom: .3rem;
    }

    .sidebar-logo {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #111827;
        color: white;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: .04em;
    }

    .sidebar-title {
        font-weight: 800;
        font-size: 1.12rem;
        line-height: 1;
    }

    .sidebar-subtitle {
        font-size: .75rem;
        color: var(--fs-muted);
        margin-top: .2rem;
    }

    /* Top header */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: .9rem 1.1rem;
        border: 1px solid var(--fs-border);
        border-radius: 18px;
        margin-bottom: 1rem;
        background: linear-gradient(
            135deg,
            rgba(99, 91, 255, .08),
            rgba(16, 185, 129, .04)
        );
    }

    .topbar-left {
        display: flex;
        align-items: center;
        gap: .8rem;
    }

    .topbar-logo {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #111827;
        color: white;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: .04em;
    }

    .topbar-title {
        font-size: 1.25rem;
        font-weight: 850;
        margin: 0;
    }

    .topbar-subtitle {
        margin: .14rem 0 0;
        font-size: .82rem;
        color: var(--fs-muted);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        padding: .42rem .75rem;
        border-radius: 999px;
        border: 1px solid rgba(22,163,74,.22);
        background: rgba(22,163,74,.07);
        color: #15803d;
        font-size: .76rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
    }

    /* Hero */
    .hero {
        padding: 2.2rem 2rem;
        border-radius: 24px;
        border: 1px solid var(--fs-border);
        background:
            radial-gradient(circle at top right, rgba(99,91,255,.22), transparent 34%),
            radial-gradient(circle at bottom left, rgba(16,185,129,.12), transparent 32%),
            linear-gradient(135deg, rgba(99,91,255,.08), rgba(255,255,255,.01));
        margin-bottom: 1.1rem;
    }

    .hero-kicker {
        display: inline-block;
        padding: .34rem .68rem;
        border-radius: 999px;
        border: 1px solid rgba(99,91,255,.18);
        background: rgba(99,91,255,.08);
        color: #594fff;
        font-size: .74rem;
        font-weight: 800;
        letter-spacing: .04em;
        text-transform: uppercase;
    }

    .hero h1 {
        font-size: clamp(2.1rem, 4vw, 3.6rem);
        line-height: 1.02;
        margin: .8rem 0 .7rem;
        letter-spacing: -.045em;
    }

    .hero p {
        max-width: 760px;
        font-size: 1.03rem;
        line-height: 1.65;
        color: var(--fs-muted);
        margin: 0;
    }

    .hero-trust {
        display: flex;
        flex-wrap: wrap;
        gap: .55rem;
        margin-top: 1rem;
    }

    .trust-chip {
        border: 1px solid var(--fs-border);
        background: rgba(255,255,255,.03);
        padding: .38rem .65rem;
        border-radius: 999px;
        font-size: .74rem;
        font-weight: 650;
    }

    /* Page headings */
    .page-title {
        font-size: 2rem;
        font-weight: 850;
        letter-spacing: -.035em;
        margin: .25rem 0 .2rem;
    }

    .page-subtitle {
        color: var(--fs-muted);
        margin-bottom: 1.2rem;
    }

    .section-title {
        font-size: 1.12rem;
        font-weight: 800;
        margin: 1rem 0 .7rem;
    }

    /* Feature cards */
    .feature-card {
        height: 100%;
        min-height: 160px;
        padding: 1.1rem;
        border-radius: 18px;
        border: 1px solid var(--fs-border);
        background: rgba(128,128,128,.025);
    }

    .feature-icon {
        font-size: 1.55rem;
        margin-bottom: .35rem;
    }

    .feature-title {
        font-weight: 800;
        margin-bottom: .3rem;
    }

    .feature-text {
        color: var(--fs-muted);
        font-size: .86rem;
        line-height: 1.55;
    }

    /* Workflow */
    .workflow-step {
        padding: 1rem;
        border: 1px solid var(--fs-border);
        border-radius: 16px;
        background: rgba(128,128,128,.025);
    }

    .workflow-number {
        width: 31px;
        height: 31px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--fs-soft);
        color: var(--fs-primary);
        font-weight: 850;
        margin-bottom: .55rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 11px;
        font-weight: 750;
        min-height: 2.55rem;
    }

    /* Inputs / upload */
    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(99,91,255,.38);
        border-radius: 16px;
        padding: .35rem;
        background: rgba(99,91,255,.025);
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
    }

    /* Footer */
    .site-footer {
        margin-top: 3rem;
        padding: 1.35rem 0 .5rem;
        border-top: 1px solid var(--fs-border);
        color: var(--fs-muted);
        font-size: .78rem;
    }

    .footer-grid {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .footer-brand {
        font-weight: 800;
        color: inherit;
    }

    .footer-note {
        margin-top: .45rem;
        font-size: .72rem;
        opacity: .82;
    }

    /* Hide anchor decorations used by markdown headings */
    a { text-decoration: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DYNAMIC LIGHT / DARK THEME
# ============================================================
if CURRENT_THEME == "dark":
    st.markdown(
        """
        <style>
        :root {
            --fs-bg: #0a0f1c;
            --fs-surface: #111827;
            --fs-surface-2: #172033;
            --fs-primary: #818cf8;
            --fs-primary-strong: #6366f1;
            --fs-accent: #2dd4bf;
            --fs-text: #f8fafc;
            --fs-muted: #94a3b8;
            --fs-border: #263247;
            --fs-hover: #1b2638;
            --fs-shadow: 0 14px 38px rgba(0,0,0,.28);
        }

        /* App canvas */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--fs-bg) !important;
            color: var(--fs-text) !important;
        }

        [data-testid="stMainBlockContainer"] {
            color: var(--fs-text) !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #0d1422 !important;
            border-right: 1px solid var(--fs-border) !important;
        }

        section[data-testid="stSidebar"] .block-container {
            background: #0d1422 !important;
        }

        section[data-testid="stSidebar"] * {
            color: var(--fs-text);
        }

        section[data-testid="stSidebar"] .sidebar-subtitle,
        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small {
            color: var(--fs-muted) !important;
        }

        /* Main text */
        .page-subtitle,
        .hero p,
        .feature-text,
        .topbar-subtitle,
        .footer-note,
        .site-footer {
            color: var(--fs-muted) !important;
        }

        /* Surfaces */
        .topbar,
        .feature-card,
        .workflow-step,
        .site-footer,
        .hero {
            background: var(--fs-surface) !important;
            border-color: var(--fs-border) !important;
            box-shadow: var(--fs-shadow);
        }

        .hero {
            background:
                radial-gradient(circle at top right, rgba(99,102,241,.24), transparent 34%),
                radial-gradient(circle at bottom left, rgba(45,212,191,.12), transparent 32%),
                #111827 !important;
        }

        .hero-kicker {
            border-color: rgba(129,140,248,.35) !important;
            background: rgba(129,140,248,.12) !important;
            color: #c7d2fe !important;
        }

        .trust-chip {
            background: #172033 !important;
            border-color: var(--fs-border) !important;
            color: #dbe4f0 !important;
        }

        .workflow-number {
            background: rgba(129,140,248,.12) !important;
            color: #a5b4fc !important;
        }

        /* Inputs */
        input,
        textarea,
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div {
            background: #111827 !important;
            color: var(--fs-text) !important;
            border-color: var(--fs-border) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #64748b !important;
        }

        [data-testid="stFileUploader"] {
            background: #111827 !important;
            border-color: #475569 !important;
        }

        [data-testid="stFileUploader"] * {
            color: var(--fs-text) !important;
        }

        /* Buttons */
        .stButton > button,
        [data-testid="stFormSubmitButton"] > button {
            background: transparent !important;
            color: var(--fs-text) !important;
            border: 1px solid var(--fs-border) !important;
        }

        .stButton > button:hover,
        [data-testid="stFormSubmitButton"] > button:hover {
            background: var(--fs-hover) !important;
            border-color: #475569 !important;
            color: #ffffff !important;
        }

        /* Primary action */
        .stButton > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button[kind="primary"] {
            background: #6366f1 !important;
            color: #ffffff !important;
            border-color: #6366f1 !important;
            box-shadow: 0 8px 22px rgba(99,102,241,.22) !important;
        }

        .stButton > button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
            background: #818cf8 !important;
            border-color: #818cf8 !important;
        }

        /* Sidebar navigation */
        section[data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: #cbd5e1 !important;
            border-color: transparent !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #141d2d !important;
            color: #ffffff !important;
            border-color: #263247 !important;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: #172033 !important;
            color: #ffffff !important;
            border-color: #2f3b51 !important;
            box-shadow: inset 3px 0 0 #818cf8 !important;
        }

        /* Status */
        .status-pill {
            background: rgba(45,212,191,.09) !important;
            border-color: rgba(45,212,191,.22) !important;
            color: #5eead4 !important;
        }

        .status-dot {
            background: #2dd4bf !important;
        }

        /* Divider */
        hr {
            border-color: var(--fs-border) !important;
        }

        /* Chat messages */
        [data-testid="stChatMessage"] {
            background: #111827 !important;
            border: 1px solid var(--fs-border) !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background: #111827 !important;
            border-color: var(--fs-border) !important;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background: #111827 !important;
            border: 1px solid var(--fs-border) !important;
            padding: 1rem !important;
            border-radius: 14px !important;
        }

        /* Code blocks */
        code {
            color: #c7d2fe !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>

        /* =====================================================
           LIGHT MODE — PREMIUM FINTECH PALETTE
           ===================================================== */

        :root {
            --fs-bg: #F7F8FC;
            --fs-surface: #FFFFFF;
            --fs-surface-soft: #FAFBFF;

            --fs-primary: #4F46E5;
            --fs-primary-hover: #4338CA;
            --fs-primary-soft: #EEF2FF;

            --fs-accent: #0F766E;
            --fs-accent-soft: #ECFDF5;

            --fs-text: #111827;
            --fs-text-secondary: #374151;
            --fs-muted: #64748B;

            --fs-border: #E5E7EB;
            --fs-border-strong: #CBD5E1;

            --fs-success: #15803D;
            --fs-success-soft: #F0FDF4;

            --fs-warning: #B45309;
            --fs-warning-soft: #FFF7ED;

            --fs-danger: #DC2626;
            --fs-danger-soft: #FEF2F2;
        }


        /* =====================================================
           MAIN APP
           ===================================================== */

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--fs-bg) !important;
            color: var(--fs-text) !important;
        }

        [data-testid="stMainBlockContainer"] {
            color: var(--fs-text) !important;
        }


        /* =====================================================
           ALL NORMAL TEXT
           Fixes washed-out / invisible text
           ===================================================== */

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stText"],
        .stText {
            color: var(--fs-text-secondary) !important;
        }

        [data-testid="stMarkdownContainer"] strong,
        [data-testid="stMarkdownContainer"] b {
            color: var(--fs-text) !important;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--fs-text) !important;
        }

        .page-title {
            color: var(--fs-text) !important;
        }

        .page-subtitle {
            color: var(--fs-muted) !important;
        }

        .section-title {
            color: var(--fs-text) !important;
        }


        /* =====================================================
           TOP HEADER
           ===================================================== */

        .topbar {
            background:
                linear-gradient(
                    135deg,
                    #FFFFFF 0%,
                    #F8FAFF 65%,
                    #F3FBF9 100%
                ) !important;

            border: 1px solid var(--fs-border) !important;
            box-shadow:
                0 4px 18px rgba(15, 23, 42, 0.04) !important;
        }

        .topbar-title {
            color: var(--fs-text) !important;
        }

        .topbar-subtitle {
            color: var(--fs-muted) !important;
        }


        /* =====================================================
           HERO SECTION
           ===================================================== */

        .hero {
            background:
                radial-gradient(
                    circle at 88% 12%,
                    rgba(79, 70, 229, 0.10),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 8% 90%,
                    rgba(15, 118, 110, 0.07),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    #FFFFFF,
                    #F8FAFF
                ) !important;

            border: 1px solid var(--fs-border) !important;
            box-shadow:
                0 10px 30px rgba(15, 23, 42, 0.05) !important;
        }

        .hero h1 {
            color: var(--fs-text) !important;
        }

        .hero p {
            color: var(--fs-muted) !important;
        }

        .hero-kicker {
            background: var(--fs-primary-soft) !important;
            color: #4338CA !important;
            border: 1px solid #C7D2FE !important;
        }


        /* =====================================================
           SMALL TRUST CHIPS
           ===================================================== */

        .trust-chip {
            background: #FFFFFF !important;
            color: var(--fs-text-secondary) !important;
            border: 1px solid var(--fs-border) !important;
        }


        /* =====================================================
           FEATURE CARDS
           ===================================================== */

        .feature-card {
            background: var(--fs-surface) !important;
            border: 1px solid var(--fs-border) !important;
            box-shadow:
                0 4px 16px rgba(15, 23, 42, 0.035) !important;
        }

        .feature-card:hover {
            border-color: #C7D2FE !important;
            box-shadow:
                0 10px 25px rgba(79, 70, 229, 0.08) !important;
        }

        .feature-title {
            color: var(--fs-text) !important;
        }

        .feature-text {
            color: var(--fs-muted) !important;
        }


        /* =====================================================
           WORKFLOW CARDS
           ===================================================== */

        .workflow-step {
            background: #FFFFFF !important;
            border: 1px solid var(--fs-border) !important;
            color: var(--fs-text) !important;
        }

        .workflow-number {
            background: var(--fs-primary-soft) !important;
            color: var(--fs-primary) !important;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid var(--fs-border) !important;
        }

        section[data-testid="stSidebar"] .block-container {
            background: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] .sidebar-title {
            color: var(--fs-text) !important;
        }

        section[data-testid="stSidebar"] .sidebar-subtitle {
            color: var(--fs-muted) !important;
        }

        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small {
            color: var(--fs-muted) !important;
        }


        /* =====================================================
           SIDEBAR NAVIGATION
           ===================================================== */

        section[data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: #475569 !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #F8FAFC !important;
            border-color: #E2E8F0 !important;
            color: #111827 !important;
        }

        section[data-testid="stSidebar"]
        .stButton > button[kind="primary"] {
            background: #EEF2FF !important;
            color: #3730A3 !important;
            border: 1px solid #E0E7FF !important;
            box-shadow: inset 3px 0 0 #4F46E5 !important;
        }


        /* =====================================================
           METRIC CARDS
           ===================================================== */

        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid var(--fs-border) !important;
            border-radius: 14px !important;
            color: var(--fs-text) !important;
            box-shadow:
                0 4px 16px rgba(15, 23, 42, 0.035) !important;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] * {
            color: var(--fs-muted) !important;
        }

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] * {
            color: var(--fs-text) !important;
            font-weight: 800 !important;
        }

        [data-testid="stMetricDelta"],
        [data-testid="stMetricDelta"] * {
            color: var(--fs-text-secondary) !important;
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        input,
        textarea,
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div {
            background: #FFFFFF !important;
            color: var(--fs-text) !important;
            border-color: var(--fs-border-strong) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #94A3B8 !important;
        }

        input:focus,
        textarea:focus {
            border-color: var(--fs-primary) !important;
            box-shadow:
                0 0 0 3px rgba(79, 70, 229, 0.10) !important;
        }


        /* =====================================================
           FILE UPLOADER
           ===================================================== */

        [data-testid="stFileUploader"] {
            background: #FFFFFF !important;
            border: 1px solid var(--fs-border) !important;
            border-radius: 14px !important;
        }

        [data-testid="stFileUploader"] * {
            color: var(--fs-text-secondary) !important;
        }


        /* =====================================================
           PRIMARY BUTTON
           ===================================================== */

        .stButton > button[kind="primary"] {
            background: #4F46E5 !important;
            color: #FFFFFF !important;
            border: 1px solid #4F46E5 !important;

            box-shadow:
                0 7px 18px rgba(79, 70, 229, 0.15) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: #4338CA !important;
            border-color: #4338CA !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
        }


        /* =====================================================
           SECONDARY BUTTON
           ===================================================== */

        .stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: var(--fs-text-secondary) !important;
            border: 1px solid var(--fs-border-strong) !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #F8FAFC !important;
            border-color: #94A3B8 !important;
            color: var(--fs-text) !important;
        }


        /* =====================================================
           EXPANDERS
           ===================================================== */

        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid var(--fs-border) !important;
            border-radius: 12px !important;
        }

        [data-testid="stExpander"] summary {
            color: var(--fs-text) !important;
            font-weight: 700 !important;
        }

        [data-testid="stExpander"] p {
            color: var(--fs-text-secondary) !important;
        }


        /* =====================================================
           ALERTS
           ===================================================== */

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] div {
            color: var(--fs-text-secondary) !important;
        }


        /* =====================================================
           CHAT
           ===================================================== */

        [data-testid="stChatMessage"] {
            background: #FFFFFF !important;
            border: 1px solid var(--fs-border) !important;
            border-radius: 14px !important;

            box-shadow:
                0 4px 14px rgba(15, 23, 42, 0.035) !important;
        }

        [data-testid="stChatMessage"] p {
            color: var(--fs-text-secondary) !important;
        }


        /* =====================================================
           PROGRESS BARS
           ===================================================== */

        [data-testid="stProgress"] > div {
            background: #E2E8F0 !important;
            border-radius: 999px !important;
        }

        [data-testid="stProgress"] [role="progressbar"] {
            background: #4F46E5 !important;
            border-radius: 999px !important;
        }


        /* =====================================================
           CONTAINERS
           ===================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #FFFFFF !important;
            border-color: var(--fs-border) !important;
        }


        /* =====================================================
           FOOTER
           ===================================================== */

        .site-footer {
            background: #FFFFFF !important;
            border-top: 1px solid var(--fs-border) !important;
            color: var(--fs-muted) !important;
        }

        .footer-brand {
            color: var(--fs-text) !important;
        }

        .footer-note {
            color: var(--fs-muted) !important;
        }


        /* =====================================================
           DIVIDERS
           ===================================================== */

        hr {
            border-color: var(--fs-border) !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_ocr" not in st.session_state:
    st.session_state.last_ocr = None

if "last_expense" not in st.session_state:
    st.session_state.last_expense = None


# ============================================================
# HELPERS
# ============================================================
def navigate(page_name: str):
    st.session_state.page = page_name
    st.rerun()


def render_footer():
    st.markdown(
        """
        <div class="site-footer">
            <div class="footer-grid">
                <div class="footer-brand">FinSight AI</div>
                <div>Personal Finance Intelligence • RAG • OCR • MySQL</div>
            </div>
            <div class="footer-note">
                FinSight AI is an educational financial assistance system. It does not guarantee investment returns or replace professional financial advice.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">F</div>
            <div>
                <div class="sidebar-title">FinSight AI</div>
                <div class="sidebar-subtitle">Personal Finance Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    nav_items = [
        "Home",
        "Dashboard",
        "Add Expense",
        "AI Advisor",
        "About FinSight",
        "Help & Safety",
    ]

    # Classic text navigation — no radio buttons and no decorative icons.
    for label in nav_items:
        is_active = st.session_state.page == label

        if st.button(
            label,
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.page = label
            st.rerun()

    st.markdown(
        """
        <style>

        /* Appearance switch */
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button {
            min-height: 38px;
            font-size: .82rem;
            letter-spacing: .01em;
        }

        /* Sidebar navigation buttons */
        section[data-testid="stSidebar"] .stButton > button {
            min-height: 42px;
            margin: 2px 0;
            padding: .42rem .7rem;
            border-radius: 8px;
            text-align: left;
            justify-content: flex-start;
            font-weight: 650;
            font-size: .92rem;
            border: 1px solid transparent;
            background: transparent;
            color: #374151;
            transition: all .16s ease;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #f5f6fa;
            border-color: #e5e7eb;
            color: #111827;
        }

        /* Active item: classic, understated */
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: #f0f1f5;
            border: 1px solid #dfe2e8;
            color: #111827;
            box-shadow: none;
            font-weight: 750;
            box-shadow: inset 3px 0 0 #635bff;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            background: #eceef3;
            color: #111827;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Appearance")
    theme_col1, theme_col2 = st.columns(2)

    with theme_col1:
        if st.button(
            "Light",
            key="theme_light",
            use_container_width=True,
            type="primary" if CURRENT_THEME == "light" else "secondary",
        ):
            st.session_state.theme = "light"
            st.rerun()

    with theme_col2:
        if st.button(
            "Dark",
            key="theme_dark",
            use_container_width=True,
            type="primary" if CURRENT_THEME == "dark" else "secondary",
        ):
            st.session_state.theme = "dark"
            st.rerun()

    st.divider()
    st.caption("DEMO ACCOUNT")
    st.markdown("**Pawan / User 1**")
    st.caption("MySQL • Aiven Cloud")

    st.write("")
    if st.button("Clear AI Chat", use_container_width=True):
        st.session_state.messages = []
        st.toast("AI chat cleared")
        st.rerun()


# ============================================================
# GLOBAL HEADER
# ============================================================
st.markdown(
    """
    <div class="topbar">
        <div class="topbar-left">
            <div class="topbar-logo">F</div>
            <div>
                <div class="topbar-title">FinSight AI</div>
                <div class="topbar-subtitle">AI-powered personal finance intelligence</div>
            </div>
        </div>
        <div class="status-pill"><span class="status-dot"></span> System Online</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HOME
# ============================================================
if st.session_state.page == "Home":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">AI Financial Assistant</div>
            <h1>Understand your money.<br>Make every decision clearer.</h1>
            <p>
                FinSight AI brings expense tracking, OCR, financial analytics and
                RAG-powered financial knowledge into one simple platform.
            </p>
            <div class="hero-trust">
                <div class="trust-chip">OCR OCR Expense Capture</div>
                <div class="trust-chip">📚 LangChain RAG</div>
                <div class="trust-chip">DB MySQL</div>
                <div class="trust-chip">AI AI Advisor</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("DATA Open Dashboard", type="primary", use_container_width=True):
            navigate("Dashboard")
    with c2:
        if st.button("OCR Add an Expense", use_container_width=True):
            navigate("Add Expense")

    st.markdown('<div class="section-title">What FinSight AI does</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    home_features = [
        ("OCR", "Capture expenses", "Upload a payment screenshot and let the OCR pipeline extract transaction information."),
        ("DATA", "Understand spending", "View spending categories, configured budgets, remaining amounts and utilization."),
        ("AI", "Ask your financial AI", "Get contextual answers using your actual financial information and retrieved financial knowledge."),
    ]

    for col, (icon, title, text) in zip((f1, f2, f3), home_features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">How the system works</div>', unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    steps = [
        ("1", "Upload", "Payment screenshot"),
        ("2", "Extract", "Vision OCR + parser"),
        ("3", "Store", "MySQL financial record"),
        ("4", "Assist", "RAG + AI response"),
    ]
    for col, (num, title, desc) in zip((w1, w2, w3, w4), steps):
        with col:
            st.markdown(
                f"""
                <div class="workflow-step">
                    <div class="workflow-number">{num}</div>
                    <b>{title}</b>
                    <div class="feature-text">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# DASHBOARD
# ============================================================
elif st.session_state.page == "Dashboard":
    st.markdown('<div class="page-title">Financial Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">A visual overview of the financial data currently stored for the demo account.</div>',
        unsafe_allow_html=True,
    )
    show_dashboard(USER_ID)


# ============================================================
# ADD EXPENSE
# ============================================================
elif st.session_state.page == "Add Expense":
    st.markdown('<div class="page-title">Add Expense</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Upload a payment screenshot and let FinSight AI turn it into a structured expense record.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, .95], gap="large")

    with left:
        st.markdown('<div class="section-title">OCR Payment Screenshot</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload screenshot",
            type=["png", "jpg", "jpeg", "webp"],
            help="Supported formats: PNG, JPG, JPEG, WEBP",
        )

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded payment screenshot", use_container_width=True)

            if st.button("⚡ Process Expense", type="primary", use_container_width=True):
                temp_path = None

                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=Path(uploaded_file.name).suffix or ".png",
                    ) as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_path = Path(temp_file.name)

                    with st.status("Processing expense...", expanded=True) as status:
                        st.write("OCR Reading payment screenshot...")
                        ocr_text = vision_transcribe(temp_path)
                        st.session_state.last_ocr = ocr_text

                        st.write("🧠 Extracting transaction details...")
                        expense = parse_expense(ocr_text)
                        st.session_state.last_expense = expense

                        st.write("💾 Saving transaction to MySQL...")
                        expense_id = save_expense(
                            expense=expense,
                            user_id=USER_ID,
                            image_path=str(temp_path),
                        )

                        status.update(
                            label="Expense processed successfully",
                            state="complete",
                        )

                    st.success(f"Expense saved successfully • Transaction ID: {expense_id}")

                except Exception as exc:
                    st.error("We could not process this screenshot.")
                    with st.expander("Technical details"):
                        st.code(f"{type(exc).__name__}: {exc}")

                finally:
                    # The backend already receives the image path. We intentionally
                    # do not delete it here so the existing application behavior is preserved.
                    pass

    with right:
        st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)
        process_steps = [
            ("1", "Upload", "Select a payment screenshot."),
            ("2", "OCR", "Read visible transaction text."),
            ("3", "Parse", "Extract amount, merchant and category."),
            ("4", "Save", "Store the structured record in MySQL."),
        ]

        for number, title, description in process_steps:
            st.markdown(
                f"""
                <div class="workflow-step" style="margin-bottom:.65rem;">
                    <div class="workflow-number">{number}</div>
                    <b>{title}</b>
                    <div class="feature-text">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.session_state.last_expense:
        st.markdown('<div class="section-title">Latest Extracted Expense</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.json(st.session_state.last_expense)

    if st.session_state.last_ocr:
        with st.expander("🔎 View last OCR output"):
            st.text(st.session_state.last_ocr)


# ============================================================
# AI ADVISOR
# ============================================================
elif st.session_state.page == "AI Advisor":
    st.markdown('<div class="page-title">AI Financial Advisor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Ask about spending, budgets, saving, goals or general financial concepts.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:
        st.info("Try: **Am I spending too much on food?** or **What is an emergency fund?**")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask FinSight AI a financial question...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("FinSight AI is thinking..."):
                try:
                    answer = get_financial_advice(
                        user_id=USER_ID,
                        question=question,
                    )
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as exc:
                    st.error("I couldn't generate an answer right now. Please try again.")
                    with st.expander("Technical details"):
                        st.code(f"{type(exc).__name__}: {exc}")

    st.caption("FinSight AI uses your stored financial data and retrieved financial knowledge. Responses are educational and may require professional verification.")


# ============================================================
# ABOUT
# ============================================================
elif st.session_state.page == "About FinSight":
    st.markdown('<div class="page-title">About FinSight AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">A project built to combine financial data, document retrieval and AI assistance in one product.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ### What is FinSight AI?

        FinSight AI is an AI-powered personal finance assistant that combines automated expense capture,
        financial analytics, a MySQL-backed financial record and a Retrieval-Augmented Generation (RAG)
        knowledge layer. The goal is to help users understand spending patterns and ask financial questions
        using both their own financial information and retrieved financial education.
        """
    )

    a1, a2, a3 = st.columns(3)
    about_cards = [
        ("OCR", "OCR", "Reads transaction information from uploaded payment screenshots."),
        ("📚", "RAG", "Retrieves relevant information from the project's financial knowledge base."),
        ("DB", "MySQL", "Stores structured expense and financial records for analysis."),
    ]
    for col, (icon, title, desc) in zip((a1, a2, a3), about_cards):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-text">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Technology</div>', unsafe_allow_html=True)
    st.markdown(
        """
        **Frontend/UI:** Streamlit  
        **AI:** Gemma + LangChain  
        **RAG:** HuggingFace Embeddings + ChromaDB  
        **Document Processing:** PyMuPDF  
        **Database:** MySQL on Aiven Cloud  
        **Expense Processing:** Vision OCR + structured expense parsing
        """
    )

    st.markdown('<div class="section-title">Project philosophy</div>', unsafe_allow_html=True)
    st.info(
        "FinSight AI is designed to separate personal financial data from general financial knowledge. "
        "The system is also instructed not to invent transactions or guarantee investment returns."
    )


# ============================================================
# HELP & SAFETY
# ============================================================
else:
    st.markdown('<div class="page-title">Help & Safety</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">A quick guide to using the application responsibly.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("OCR How do I add an expense?", expanded=True):
        st.write(
            "Open Add Expense, upload a payment screenshot, and click Process Expense. "
            "FinSight AI will run OCR, parse the transaction and save the structured record."
        )

    with st.expander("AI What can I ask the AI Advisor?"):
        st.write(
            "You can ask about your spending, configured budgets, saving concepts, emergency funds, "
            "financial goals and other supported financial-education topics."
        )

    with st.expander("🔐 Does the AI invent financial data?"):
        st.write(
            "The advisor prompt instructs the model to use the stored financial data for personal-finance questions, "
            "use RAG for general financial education, and avoid inventing transactions, amounts or budgets."
        )

    with st.expander("⚠️ Is this professional investment advice?"):
        st.warning(
            "No. FinSight AI is an educational financial assistance project. It should not be treated as a guarantee, "
            "personalized investment recommendation or replacement for a qualified financial professional."
        )

    with st.expander("🧪 Demo / project limitations"):
        st.write(
            "This submission uses a demo user account. Authentication, full multi-user account management, "
            "advanced persistent chat memory and additional production-grade controls can be added in future versions."
        )


# ============================================================
# GLOBAL FOOTER
# ============================================================
render_footer()
