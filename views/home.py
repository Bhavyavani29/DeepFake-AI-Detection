import base64
import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st
from views.shared import go_to, show_login_dialog

load_dotenv()

# Point this at your own image, or override with HERO_IMAGE_PATH in .env
HERO_IMAGE_PATH = os.getenv("HERO_IMAGE_PATH", "assets/hero_image.png")


def _load_image_as_data_uri(path: str) -> str | None:
    """Read a local image file and return it as a base64 data URI, or None
    if the file doesn't exist yet."""
    p = Path(path)

    if not p.exists():
        return None

    ext = p.suffix.lstrip(".").lower()

    if ext in ("jpg", "jpeg"):
        mime = "image/jpeg"
    elif ext == "png":
        mime = "image/png"
    elif ext == "webp":
        mime = "image/webp"
    else:
        mime = f"image/{ext}"

    data = base64.b64encode(p.read_bytes()).decode("utf-8")

    return f"data:{mime};base64,{data}"


def _hero_graphic_svg() -> str:
    """
    Original abstract face-scan illustration (no copyrighted or stock imagery) —
    a glowing grid over a face-like outline, evoking AI analysis.
    """
    return """
    <svg viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.9"/>
                <stop offset="100%" stop-color="#14b8a6" stop-opacity="0.9"/>
            </linearGradient>
            <radialGradient id="glow" cx="50%" cy="45%" r="60%">
                <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
            </radialGradient>
        </defs>

        <circle cx="210" cy="200" r="190" fill="url(#glow)"/>

        <ellipse
            cx="210"
            cy="190"
            rx="110"
            ry="140"
            fill="none"
            stroke="url(#g1)"
            stroke-width="2"
            opacity="0.55"
        />

        <g stroke="url(#g1)" stroke-width="1" opacity="0.35">
            <line x1="100" y1="80" x2="100" y2="320"/>
            <line x1="150" y1="60" x2="150" y2="340"/>
            <line x1="210" y1="50" x2="210" y2="350"/>
            <line x1="270" y1="60" x2="270" y2="340"/>
            <line x1="320" y1="80" x2="320" y2="320"/>

            <line x1="70" y1="130" x2="350" y2="130"/>
            <line x1="60" y1="190" x2="360" y2="190"/>
            <line x1="70" y1="250" x2="350" y2="250"/>
        </g>

        <circle cx="165" cy="175" r="6" fill="#22d3ee"/>
        <circle cx="255" cy="175" r="6" fill="#22d3ee"/>

        <path
            d="M180 250 Q210 275 240 250"
            stroke="url(#g1)"
            stroke-width="3"
            fill="none"
            stroke-linecap="round"
        />

        <rect x="60" y="60" width="30" height="2" fill="#22d3ee"/>
        <rect x="60" y="60" width="2" height="30" fill="#22d3ee"/>

        <rect x="330" y="330" width="30" height="2" fill="#14b8a6"/>
        <rect x="358" y="300" width="2" height="30" fill="#14b8a6"/>

        <text
            x="210"
            y="395"
            text-anchor="middle"
            fill="#64748b"
            font-size="13"
            font-family="monospace"
        >
            ANALYZING FACIAL PATTERNS...
        </text>
    </svg>
    """


def render():

    # =========================================================
    # HOME PAGE BACKGROUND IMAGE
    # =========================================================

    image_data_uri = _load_image_as_data_uri(HERO_IMAGE_PATH)

    if image_data_uri:

        st.markdown(
            f"""
            <style>

            /* Home page background image */
            .stApp {{
                background-image:
                    linear-gradient(
                        90deg,
                        rgba(8, 8, 20, 0.96) 0%,
                        rgba(8, 8, 20, 0.82) 35%,
                        rgba(8, 8, 20, 0.48) 70%,
                        rgba(8, 8, 20, 0.30) 100%
                    ),
                    url("{image_data_uri}");

                background-size: cover;
                background-position: center right;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Keep Streamlit containers transparent */
            [data-testid="stAppViewContainer"] {{
                background: transparent !important;
            }}

            [data-testid="stMain"] {{
                background: transparent !important;
            }}

            </style>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================
    # ORIGINAL HOME CONTENT — UNCHANGED
    # =========================================================

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero-title">
                Protect the <span class="accent">Truth</span><br/>
                Detect the <span class="accent">Fake</span>
            </div>
            <div class="hero-sub">
                AI-powered deepfake detection that analyzes face images to flag
                likely AI-generated or manipulated content — with a visual
                explanation of exactly what the model noticed.
            </div>
            """,
            unsafe_allow_html=True,
        )

        b1, b2, _ = st.columns([1.3, 1, 2])

        with b1:
            st.markdown(
                '<div class="primary-btn">',
                unsafe_allow_html=True
            )

            if st.button(
                "Start Detection",
                key="hero_start"
            ):
                go_to("detect")
                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with b2:
            st.markdown(
                '<div class="outline-btn">',
                unsafe_allow_html=True
            )

            if st.button(
                "Login",
                key="hero_login"
            ):
                show_login_dialog()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    # =========================================================
    # RIGHT COLUMN
    # =========================================================
    # No image is displayed here anymore.
    # The hero image is now the background.
    # =========================================================

    with right:
        st.empty()

    # =========================================================
    # ORIGINAL CONTENT — UNCHANGED
    # =========================================================

    st.markdown(
        "<div style='height:2.5rem'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Why DeepSafe</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">Built for anyone who needs a fast, explainable second opinion on whether a face image is real.</div>',
        unsafe_allow_html=True,
    )

    features = [
        (
            "⚡",
            "Fast Analysis",
            "Get a verdict with confidence scores in under a second, right in your browser."
        ),
        (
            "🔍",
            "Explainable Results",
            "A Grad-CAM heatmap shows exactly which regions influenced the model's decision."
        ),
        (
            "📊",
            "Batch Screening",
            "Upload a whole folder of images and get a summary table in one pass."
        ),
    ]

    cols = st.columns(3, gap="medium")

    for col, (icon, title, desc) in zip(cols, features):

        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="icon-circle">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )