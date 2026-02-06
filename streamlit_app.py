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


st.set_page_config(page_title="Cattle Disease AI", layout="centered")

st.title("Cattle Disease AI")
st.caption("Streamlit UI mockup for the FastAPI prediction service.")

api_base_url = st.sidebar.text_input(
    "API Base URL",
    value=os.getenv("API_BASE_URL", "https://cattle-disease-ai.onrender.com"),
)
include_explain = st.sidebar.checkbox("Include Grad-CAM heatmap", value=True)

st.subheader("Clinical Symptoms (UI mockup)")
st.caption("These inputs are captured for the UI mockup; the current API uses image-only input.")

col1, col2, col3 = st.columns(3)
with col1:
    fever = st.checkbox("Fever")
    nodules = st.checkbox("Skin nodules")
with col2:
    mouth_sores = st.checkbox("Mouth sores")
    nasal_discharge = st.checkbox("Nasal discharge")
with col3:
    cough = st.checkbox("Cough")
    swollen_lymph = st.checkbox("Swollen lymph nodes")

symptoms_summary = {
    "fever": fever,
    "nodules": nodules,
    "mouth_sores": mouth_sores,
    "nasal_discharge": nasal_discharge,
    "cough": cough,
    "swollen_lymph": swollen_lymph,
}

st.write("Selected symptoms:", ", ".join([k.replace("_", " ") for k, v in symptoms_summary.items() if v]) or "None")

st.write("Upload a cattle image and run a prediction.")

uploaded_file = st.file_uploader(
    "Image file",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Input image", use_column_width=True)

    if st.button("Predict"):
        with st.spinner("Calling the API..."):
            try:
                payload = {
                    "image_base64": _encode_image(image),
                    "symptoms": [
                        int(symptoms_summary["fever"]),
                        int(symptoms_summary["nodules"]),
                        int(symptoms_summary["mouth_sores"]),
                        int(symptoms_summary["nasal_discharge"]),
                        int(symptoms_summary["cough"]),
                        int(symptoms_summary["swollen_lymph"]),
                    ],
                }
                endpoint = "/predict-explain" if include_explain else "/predict"
                response = requests.post(
                    _api_url(api_base_url, endpoint),
                    json=payload,
                    timeout=60,
                )
                if not response.ok:
                    st.error(f"API error {response.status_code}: {response.text}")
                else:
                    data = response.json()
                    st.subheader("Prediction")
                    st.write("Class:", data.get("class_label"))
                    st.write("Confidence:", data.get("confidence"))

                    prediction = data.get("prediction")
                    if isinstance(prediction, list):
                        st.write("Probabilities:")
                        st.bar_chart(prediction)
                    else:
                        st.write("Score:", prediction)

                    explain = data.get("explainability")
                    if explain and explain.get("heatmap_png_base64"):
                        heatmap_bytes = base64.b64decode(explain["heatmap_png_base64"])
                        heatmap_img = Image.open(io.BytesIO(heatmap_bytes))
                        st.subheader("Grad-CAM Heatmap")
                        st.image(heatmap_img, caption="Explainability heatmap", use_column_width=True)
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
else:
    st.info("Upload a JPG or PNG image to get started.")
