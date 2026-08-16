import streamlit as st
from views.shared import go_to


def render():
    st.markdown(
        "<div style='height:1.5rem'></div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1, 1.1, 1])

    with c2:
        st.markdown(
            """
            <div class="feature-card" style="text-align:center;">
                <div class="icon-circle" style="margin:0 auto 0.8rem auto;">
                    🔐
                </div>

                <h4>Welcome back</h4>

                <p>
                    Sign in to save your detection history across sessions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:1rem'></div>",
            unsafe_allow_html=True
        )

        # Email
        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email"
        )

        # Password
        password = st.text_input(
            "Password",
            type="password",
            placeholder="••••••••",
            key="login_password"
        )

        st.markdown(
            '<div class="primary-btn">',
            unsafe_allow_html=True
        )

        if st.button(
            "Sign In",
            key="login_submit",
            use_container_width=True
        ):
            if email.strip() and password.strip():

                # UI-only login.
                # No credentials are stored anywhere.
                st.session_state.logged_in = True
                st.session_state.logged_in_email = email.strip()

                st.success("Login successful!")

            else:
                st.error("Please enter both email and password.")

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='height:0.6rem'></div>",
            unsafe_allow_html=True
        )

        if st.button(
            "← Back to Home",
            key="login_back",
            use_container_width=True
        ):
            go_to("home")
            st.rerun()