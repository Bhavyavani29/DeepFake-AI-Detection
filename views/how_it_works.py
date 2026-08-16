import streamlit as st
from views.shared import go_to


def render():
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">From upload to verdict in four steps.</div>',
        unsafe_allow_html=True,
    )

    steps = [
        ("1", "📤", "Upload an Image", "Choose a face photo (JPG or PNG) — one at a time, or a whole batch."),
        ("2", "🧮", "Preprocessing", "The image is resized, normalized, and converted into the tensor format the model expects."),
        ("3", "🧠", "Model Inference", "A trained CNN scores the image and outputs a real/fake probability."),
        ("4", "📊", "Explained Result", "You get a verdict, confidence gauges, and a Grad-CAM heatmap showing what drove the decision."),
    ]

    cols = st.columns(4, gap="medium")
    for col, (num, icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div class="step-card">
                    <div class="icon-circle">{icon}</div>
                    <h4>{num}. {title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    c, _ = st.columns([1, 3])
    with c:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Try It Now", key="how_try"):
            go_to("detect")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
