"""
Shared visual chrome: global CSS, top navbar, and footer.
Kept separate so every page looks consistent without repeating code.
"""

import streamlit as st


NAV_ITEMS = [
    ("home", "Home"),
    ("about", "About"),
    ("how", "How It Works"),
    ("detect", "Detection"),
]

BRAND_NAME = "DeepSafe"


def inject_global_css():
    st.markdown(
        """
        <style>

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .stApp {
            background: radial-gradient(
                circle at 80% 0%,
                #0f1b2e 0%,
                #060a12 55%,
                #05070d 100%
            );
        }

        .block-container {
            padding-top: 1.2rem;
            max-width: 1200px;
        }


        /* =====================================================
           NAVBAR
           ===================================================== */

        .navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.9rem 0.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 1rem;
        }

        .brand {
            font-size: 1.5rem;
            font-weight: 800;
            color: white;
        }

        .brand span {
            color: #22d3ee;
        }


        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
            background: transparent;
            border: none;
            color: #cbd5e1;
            font-weight: 500;
            padding: 0.4rem 0.9rem;
            transition: color 0.15s ease;
        }

        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
            color: #22d3ee;
            background: rgba(34, 211, 238, 0.06);
        }

        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:focus {
            box-shadow: none !important;
        }

        .nav-active button {
            color: #22d3ee !important;
            font-weight: 700 !important;
        }


        /* =====================================================
           HERO
           ===================================================== */

        .hero-title {
            font-size: 3.6rem;
            font-weight: 800;
            line-height: 1.15;
            color: white;
            margin-bottom: 1rem;
        }

        .hero-title .accent {
            background: linear-gradient(
                135deg,
                #22d3ee,
                #14b8a6
            );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-sub {
            color: #94a3b8;
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 1.8rem;
            max-width: 540px;
        }


        /* =====================================================
           HOME BUTTONS
           ===================================================== */

        .primary-btn button {
            background: linear-gradient(
                135deg,
                #22d3ee,
                #14b8a6
            ) !important;

            color: #04121a !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 0.7rem 1.6rem !important;
            font-size: 1rem !important;
        }

        .outline-btn button {
            background: transparent !important;
            color: #22d3ee !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            border: 1px solid #22d3ee !important;
            padding: 0.7rem 1.6rem !important;
            font-size: 1rem !important;
        }


        /* =====================================================
           HERO IMAGE
           ===================================================== */

        .hero-image-wrap {
            position: relative;
            border-radius: 20px;
            overflow: hidden;
            box-shadow:
                0 20px 60px rgba(0,0,0,0.55),
                0 0 90px rgba(34,211,238,0.10);
        }

        .hero-image {
            width: 100%;
            display: block;
            filter:
                brightness(0.6)
                contrast(1.15)
                saturate(0.85);
        }

        .hero-image-overlay {
            position: absolute;
            inset: 0;

            background:
                linear-gradient(
                    160deg,
                    rgba(5,8,15,0.80) 0%,
                    rgba(8,16,28,0.45) 45%,
                    rgba(10,25,35,0.30) 100%
                );

            mix-blend-mode: multiply;
        }

        .hero-image-glow {
            position: absolute;
            inset: 0;

            background:
                radial-gradient(
                    circle at 75% 15%,
                    rgba(34,211,238,0.35),
                    transparent 55%
                ),
                radial-gradient(
                    circle at 20% 85%,
                    rgba(20,184,166,0.20),
                    transparent 50%
                );

            mix-blend-mode: screen;
        }


        /* =====================================================
           GENERIC SECTIONS
           ===================================================== */

        .section-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.5rem;
        }

        .section-sub {
            color: #94a3b8;
            font-size: 1.05rem;
            margin-bottom: 2rem;
            max-width: 640px;
        }

        .feature-card,
        .step-card {
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 16px;
            padding: 1.5rem;
            height: 100%;
        }

        .feature-card h4,
        .step-card h4 {
            color: white;
            margin-top: 0.6rem;
        }

        .feature-card p,
        .step-card p {
            color: #94a3b8;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .icon-circle {
            width: 46px;
            height: 46px;
            border-radius: 12px;

            background: linear-gradient(
                135deg,
                rgba(34,211,238,0.18),
                rgba(20,184,166,0.18)
            );

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 1.4rem;
        }


        /* =====================================================
           FOOTER
           ===================================================== */

        .site-footer {
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid rgba(255,255,255,0.06);
            color: #64748b;
            font-size: 0.85rem;
            text-align: center;
        }


        /* =====================================================
           LOGIN DIALOG
           ===================================================== */

        div[data-testid="stDialog"] {
            background: #0f172a !important;
            border-radius: 18px !important;
        }

        div[data-testid="stDialog"] h2 {
            color: white !important;
        }

        .login-title {
            color: white;
            font-size: 1.7rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }

        .login-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def go_to(page_key: str):
    st.session_state.page = page_key


# =========================================================
# LOGIN DIALOG
# =========================================================

@st.dialog("Login")
def show_login_dialog():

    st.markdown(
        """
        <div class="login-title">
            Welcome to DeepSafe
        </div>

        <div class="login-subtitle">
            Enter your email and password to continue.
        </div>
        """,
        unsafe_allow_html=True,
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email",
        key="dialog_login_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="dialog_login_password",
    )

    if st.button(
        "Login",
        type="primary",
        use_container_width=True,
        key="dialog_login_submit",
    ):

        # Check email
        if not email.strip():

            st.error("Please enter your email.")

        # Basic email validation
        elif "@" not in email or "." not in email:

            st.error("Please enter a valid email address.")

        # Check password
        elif not password.strip():

            st.error("Please enter your password.")

        else:

            # -------------------------------------------------
            # UI-ONLY LOGIN
            # No database or authentication backend is used.
            # -------------------------------------------------

            st.session_state.logged_in = True
            st.session_state.logged_in_email = email.strip()

            # Close the dialog by rerunning the application.
            st.rerun()


# =========================================================
# NAVBAR
# =========================================================

def render_navbar():

    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Get Started has been removed.
    #
    # Navbar:
    # DeepSafe | Home | About | How It Works | Detection | Login

    left, *nav_cols, login_col = st.columns(
        [2, 1, 1, 1, 1, 0.9]
    )

    with left:

        st.markdown(
            '<div class="brand">Deep<span>Safe</span></div>',
            unsafe_allow_html=True,
        )

    for col, (key, label) in zip(nav_cols, NAV_ITEMS):

        with col:

            active = st.session_state.page == key

            wrapper_class = "nav-active" if active else ""

            st.markdown(
                f'<div class="{wrapper_class}">',
                unsafe_allow_html=True,
            )

            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
            ):

                go_to(key)
                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

    with login_col:

        if st.button(
            "Login",
            key="nav_login",
            use_container_width=True,
        ):

            show_login_dialog()


# =========================================================
# FOOTER
# =========================================================

def render_footer():

    st.markdown(
        f"""
        <div class="site-footer">
            © 2026 {BRAND_NAME} · AI-based deepfake screening —
            not a forensic or legal verification tool.
        </div>
        """,
        unsafe_allow_html=True,
    )