import base64
import io
import os

import requests
import streamlit as st
from PIL import Image


def _encode_image(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _api_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


st.set_page_config(page_title="Cattle Disease AI", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        color: #475569;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .section {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.06);
    }
    .label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748b;
        font-weight: 700;
    }
    .value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0.25rem 0 0.5rem 0;
    }
    .note {
        color: #334155;
        font-weight: 600;
    }
    .status-good {
        background: #dcfce7;
        color: #166534;
        padding: 0.5rem 0.75rem;
        border-radius: 10px;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .status-warn {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem 0.75rem;
        border-radius: 10px;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .pill {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        background: #e2e8f0;
        color: #0f172a;
        font-weight: 700;
        font-size: 0.85rem;
        margin: 0.25rem 0.25rem 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Cattle Disease AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Simple, readable UI for field diagnosis.</div>',
    unsafe_allow_html=True,
)

api_base_url = st.sidebar.text_input(
    "API Base URL",
    value=os.getenv("API_BASE_URL", "https://cattle-disease-ai.onrender.com"),
)
include_explain = st.sidebar.checkbox("Include Grad-CAM heatmap", value=True)

if st.sidebar.button("Check API health"):
    try:
        health = requests.get(_api_url(api_base_url, "/health"), timeout=20)
        if health.ok:
            st.sidebar.success("API is healthy")
        else:
            st.sidebar.error(f"API error {health.status_code}")
    except requests.RequestException as exc:
        st.sidebar.error(f"API check failed: {exc}")

st.sidebar.markdown("---")
st.sidebar.markdown("Symptom Inputs")

sym_nodules = st.sidebar.checkbox("Skin Nodules (LSD)", value=False)
sym_mouth = st.sidebar.checkbox("Mouth/Hoof Sores (FMD)", value=False)
sym_cough = st.sidebar.checkbox("Coughing (CBPP)", value=False)
sym_swollen = st.sidebar.checkbox("Swollen Neck/Fever (ECF)", value=False)

if st.sidebar.button("Clear results"):
    st.session_state["last_response"] = None
    st.session_state["last_image"] = None

if "last_response" not in st.session_state:
    st.session_state["last_response"] = None
if "last_image" not in st.session_state:
    st.session_state["last_image"] = None

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("### Upload and Diagnose")
    st.markdown("Upload a clear side-profile image of the cattle.")
    uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Captured image", use_column_width=True)
    else:
        image = None

    if st.button("Run Diagnosis", use_container_width=True, type="primary"):
        if image is None:
            st.warning("Please upload a cattle image first.")
        else:
            if not api_base_url.strip():
                st.error("Please provide a valid API base URL in the sidebar.")
                st.markdown('</div>', unsafe_allow_html=True)
                st.stop()
            symptoms = [
                int(sym_swollen),
                int(sym_nodules),
                int(sym_mouth),
                0,
                int(sym_cough),
                int(sym_swollen),
            ]
            payload = {
                "image_base64": _encode_image(image),
                "symptoms": symptoms,
            }
            endpoint = "/predict-explain" if include_explain else "/predict"
            try:
                with st.spinner("Calling the API..."):
                    response = requests.post(
                        _api_url(api_base_url, endpoint),
                        json=payload,
                        timeout=60,
                    )
                if not response.ok:
                    st.error(f"API error {response.status_code}: {response.text}")
                else:
                    st.session_state["last_response"] = response.json()
                    st.session_state["last_image"] = image
                    st.markdown(
                        '<div class="status-good">Diagnosis complete. See results on the right.</div>',
                        unsafe_allow_html=True,
                    )
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("### Results")
    response = st.session_state.get("last_response")
    image = st.session_state.get("last_image")

    if response is None or image is None:
        st.markdown(
            '<div class="status-warn">Run a diagnosis to see results.</div>',
            unsafe_allow_html=True,
        )
    else:
        label = response.get("class_label") or "Unknown"
        st.markdown('<div class="label">Probable Disease</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="value">{label}</div>', unsafe_allow_html=True)

        confidence = response.get("confidence")
        if isinstance(confidence, (int, float)):
            st.progress(min(max(float(confidence), 0.0), 1.0))
            st.caption(f"Confidence Score: {float(confidence):.2f}")

        st.image(image, caption="Captured image", use_column_width=True)

        explain = response.get("explainability")
        if explain and explain.get("heatmap_png_base64"):
            heatmap_bytes = base64.b64decode(explain["heatmap_png_base64"])
            heatmap_img = Image.open(io.BytesIO(heatmap_bytes))
            st.image(heatmap_img, caption="Grad-CAM heatmap", use_column_width=True)

        st.markdown("#### Reported Symptoms")
        symptom_labels = []
        if sym_nodules:
            symptom_labels.append("Skin nodules")
        if sym_mouth:
            symptom_labels.append("Mouth/hoof sores")
        if sym_cough:
            symptom_labels.append("Coughing")
        if sym_swollen:
            symptom_labels.append("Swollen neck/fever")
        if symptom_labels:
            for label_text in symptom_labels:
                st.markdown(f'<span class="pill">{label_text}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="pill">No symptoms selected</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.button("Save Case Offline", use_container_width=True)
        st.button("Sync to Vet", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
