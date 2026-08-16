import io
import os
from datetime import datetime

import numpy as np
import torch
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from utils.model_utils import load_model, preprocess_image, predict, GradCAM, CLASSES

MODEL_PATH = os.getenv("MODEL_PATH", "model/best_model.pth")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@st.cache_resource(show_spinner=False)
def get_model():
    return load_model(MODEL_PATH, DEVICE)


def make_gauge(value: float, title: str, color: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value * 100,
            number={"suffix": "%", "font": {"size": 30}},
            title={"text": title, "font": {"size": 15}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "gray"},
                "bar": {"color": color},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "rgba(255,255,255,0.05)"},
                    {"range": [50, 100], "color": "rgba(255,255,255,0.08)"},
                ],
            },
        )
    )
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    return fig


def overlay_heatmap(pil_img: Image.Image, cam: np.ndarray) -> Image.Image:
    import matplotlib.cm as cm

    cam_img = Image.fromarray(np.uint8(cam * 255)).resize(pil_img.size, Image.BILINEAR)
    cam_arr = np.array(cam_img) / 255.0
    heatmap = cm.jet(cam_arr)[:, :, :3]
    heatmap = (heatmap * 255).astype(np.uint8)

    base = np.array(pil_img.convert("RGB")).astype(np.float32)
    blended = base * 0.55 + heatmap.astype(np.float32) * 0.45
    return Image.fromarray(np.uint8(np.clip(blended, 0, 255)))


def run_inference(model, pil_img: Image.Image, want_gradcam: bool):
    tensor = preprocess_image(pil_img, DEVICE)
    result = predict(model, tensor)

    heatmap_img = None
    if want_gradcam:
        try:
            gradcam = GradCAM(model)
            class_idx = CLASSES.index(result["label"])
            cam = gradcam.generate(tensor, class_idx)
            heatmap_img = overlay_heatmap(pil_img, cam)
        except Exception:
            heatmap_img = None

    return result, heatmap_img


def render():
    st.markdown('<div class="section-title">🕵️ Run Detection</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Upload a face image below and DeepSafe will estimate whether it\'s real or AI-generated.</div>',
        unsafe_allow_html=True,
    )

    if "history" not in st.session_state:
        st.session_state.history = []

    with st.expander("⚙️ Detection settings"):
        conf_threshold = st.slider("Flag as low-confidence below", 0.5, 0.99, 0.60, 0.01)
        show_gradcam = st.checkbox("Show Grad-CAM heatmap (why the model decided this)", value=True)
        st.caption(f"Model weights: `{MODEL_PATH}` · Device: {DEVICE.type.upper()}")

    if not os.path.exists(MODEL_PATH):
        st.warning(
            f"No model weights found at **{MODEL_PATH}**. Place `best_model.pth` there, "
            "or set `MODEL_PATH=/path/to/best_model.pth` in a `.env` file, then rerun."
        )
        return

    try:
        model = get_model()
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return

    tab_single, tab_batch = st.tabs(["🖼️ Single Image", "📁 Batch Upload"])

    # ---------------------------------------------------------------- SINGLE
    with tab_single:
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("#### Upload")
            uploaded_file = st.file_uploader(
                "Drop a face image (JPG / PNG)", type=["jpg", "jpeg", "png"], key="single"
            )

            if uploaded_file:
                try:
                    pil_image = Image.open(io.BytesIO(uploaded_file.getvalue())).convert("RGB")
                except Exception:
                    st.error("Couldn't read that file — is it a valid image?")
                    pil_image = None

                if pil_image:
                    st.image(pil_image, caption=uploaded_file.name, use_container_width=True)
                    analyze = st.button("🔍 Analyze Image", type="primary", use_container_width=True)

                    if analyze:
                        with st.spinner("Running inference..."):
                            result, heatmap_img = run_inference(model, pil_image, show_gradcam)
                        st.session_state["last_result"] = result
                        st.session_state["last_heatmap"] = heatmap_img
                        st.session_state["last_name"] = uploaded_file.name
                        st.session_state.history.append(
                            {"name": uploaded_file.name, **{k: v for k, v in result.items()}}
                        )

        with col2:
            st.markdown("#### Result")
            if "last_result" in st.session_state:
                result = st.session_state["last_result"]
                label = result["label"]
                conf = result["confidence"]

                verdict_class = "verdict-fake" if label == "fake" else "verdict-real"
                emoji = "🚨" if label == "fake" else "✅"

                st.markdown(
                    f"""
                    <div class="verdict-box {verdict_class}">
                        <div class="verdict-label">{emoji} {label.upper()}</div>
                        <div class="verdict-conf">{conf*100:.2f}% confidence</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if conf < conf_threshold:
                    st.warning(
                        "⚠️ Low-confidence prediction — treat this result cautiously and "
                        "consider it inconclusive."
                    )

                g1, g2 = st.columns(2)
                with g1:
                    st.plotly_chart(
                        make_gauge(result["fake_prob"], "Fake probability", "#ef4444"),
                        use_container_width=True,
                    )
                with g2:
                    st.plotly_chart(
                        make_gauge(result["real_prob"], "Real probability", "#22c55e"),
                        use_container_width=True,
                    )

                if show_gradcam and st.session_state.get("last_heatmap") is not None:
                    with st.expander("🔥 Grad-CAM — where the model looked", expanded=True):
                        st.image(
                            st.session_state["last_heatmap"],
                            caption="Warmer regions influenced the prediction more",
                            use_container_width=True,
                        )

                report = (
                    f"DeepSafe Detection Report\n"
                    f"{'='*30}\n"
                    f"File: {st.session_state.get('last_name', 'unknown')}\n"
                    f"Verdict: {label.upper()}\n"
                    f"Confidence: {conf*100:.2f}%\n"
                    f"Fake probability: {result['fake_prob']*100:.2f}%\n"
                    f"Real probability: {result['real_prob']*100:.2f}%\n"
                    f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                st.download_button(
                    "⬇️ Download Report",
                    report,
                    file_name=f"deepfake_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True,
                )
            else:
                st.info("Upload an image and click **Analyze Image** to see results here.")

    # ----------------------------------------------------------------- BATCH
    with tab_batch:
        st.markdown("#### Analyze multiple images at once")
        batch_files = st.file_uploader(
            "Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="batch"
        )

        if batch_files and st.button("🔍 Analyze All", type="primary"):
            rows = []
            progress = st.progress(0.0)
            for i, f in enumerate(batch_files):
                try:
                    pil_img = Image.open(io.BytesIO(f.getvalue())).convert("RGB")
                    result, _ = run_inference(model, pil_img, want_gradcam=False)
                    rows.append(
                        {
                            "File": f.name,
                            "Verdict": result["label"].upper(),
                            "Confidence": f"{result['confidence']*100:.2f}%",
                            "Fake %": f"{result['fake_prob']*100:.2f}",
                            "Real %": f"{result['real_prob']*100:.2f}",
                        }
                    )
                except Exception as e:
                    rows.append({"File": f.name, "Verdict": "ERROR", "Confidence": str(e), "Fake %": "-", "Real %": "-"})
                progress.progress((i + 1) / len(batch_files))

            st.dataframe(rows, use_container_width=True)

            fake_count = sum(1 for r in rows if r["Verdict"] == "FAKE")
            real_count = sum(1 for r in rows if r["Verdict"] == "REAL")
            c1, c2 = st.columns(2)
            c1.metric("🔴 Flagged Fake", fake_count)
            c2.metric("🟢 Flagged Real", real_count)

    if st.session_state.history:
        with st.expander("🕒 Recent predictions this session"):
            for h in reversed(st.session_state.history[-8:]):
                icon = "🔴" if h["label"] == "fake" else "🟢"
                st.caption(f"{icon} {h['name']} — {h['label'].upper()} ({h['confidence']*100:.1f}%)")
