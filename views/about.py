import streamlit as st


def render():
    st.markdown('<div class="section-title">About DeepSafe</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">A student-built deepfake screening tool, trained on real vs. AI-generated face datasets.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🎯 The Problem</h4>
                <p>
                AI-generated and manipulated face images are increasingly hard to
                tell apart from real photos, which fuels misinformation, fraud,
                and identity abuse. Most people have no quick way to check a
                suspicious image before sharing or trusting it.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🧠 The Approach</h4>
                <p>
                DeepSafe uses a convolutional neural network trained on labeled
                real/fake face datasets to estimate the likelihood an image is
                AI-generated, and pairs that verdict with a Grad-CAM heatmap so
                the result isn't just a black-box number.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="feature-card">
            <h4>⚠️ Honest Limitations</h4>
            <p>
            This is a research/demo project, not a forensic-grade or legally
            admissible detector. Accuracy depends heavily on the training data
            and will vary across newer generation methods it hasn't seen.
            Treat every result as a probability estimate, not a certainty —
            and corroborate any high-stakes decision with additional verification.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
