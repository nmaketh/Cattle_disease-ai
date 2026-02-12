import os
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

# ----------------------------
# CONFIG (EDIT THESE)
# ----------------------------
MODEL_PATH = "ml/model/best_fusion_model.keras"      #
TFLITE_PATH = "Cattle disease diagnose"    # optional

IMG_SIZE = (224, 224)

# IMPORTANT: Must match your model output index order
CLASS_NAMES = ["Normal", "LSD", "FMD"]  #

# Optional: provide labels for symptoms. If length != model symptom dim, app will auto-generate labels.
SYMPTOM_LABELS = [
    # Example (you can change to your real 8 symptom names)
    "Fever",
    "Excessive Salivation",
    "Mouth Lesions",
    "Foot Lesions",
    "Lameness",
    "Skin Nodules",
    "Nasal Discharge",
    "Loss of Appetite",
]

DEFAULT_USE_TFLITE = False


# ----------------------------
# PAGE + STYLE
# ----------------------------
st.set_page_config(page_title="Cattle Disease AI", page_icon="🐄", layout="wide")

CUSTOM_CSS = """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.card {
  border: 1px solid rgba(49, 51, 63, 0.15);
  border-radius: 18px;
  padding: 18px 18px;
  background: rgba(255,255,255,0.70);
  box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}
.card h3 { margin: 0 0 10px 0; }
.muted { color: rgba(49,51,63,0.65); font-size: 0.92rem; }

.badge {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.85rem;
  border: 1px solid rgba(49, 51, 63, 0.15);
  background: rgba(240, 242, 246, 0.9);
}

.hr {
  height: 1px;
  background: rgba(49, 51, 63, 0.12);
  margin: 10px 0 16px 0;
}

.stButton>button {
  border-radius: 12px;
  padding: 0.65rem 1rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------
# LOADERS
# ----------------------------
@st.cache_resource
def load_keras_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Keras model not found: {path}")
    return tf.keras.models.load_model(path)

@st.cache_resource
def load_tflite_interpreter(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"TFLite model not found: {path}")
    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()
    return interpreter

@st.cache_resource
def get_model_io_info():
    """
    Detect symptom input dimension from the model to avoid (1,10) vs (None,8) errors.
    We assume:
      - One input is image: (None,224,224,3)
      - One input is symptoms: (None,N)
    """
    model = load_keras_model(MODEL_PATH)
    image_shape = None
    symptom_dim = None

    for inp in model.inputs:
        shape = tuple(inp.shape)
        if len(shape) == 4 and shape[1] == 224 and shape[2] == 224 and shape[3] == 3:
            image_shape = shape
        if len(shape) == 2:
            symptom_dim = int(shape[-1])

    if symptom_dim is None:
        raise RuntimeError("Could not detect symptom input dimension. Model may not be multimodal.")
    if image_shape is None:
        # still allow; image shape might be dynamic, but we expect 224
        image_shape = ("Unknown",)

    return {
        "symptom_dim": symptom_dim,
        "image_input_shape": image_shape,
        "output_dim": int(model.outputs[0].shape[-1]),
    }


# ----------------------------
# PREPROCESS + INFERENCE
# ----------------------------
def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    img = pil_img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)  # (1,224,224,3)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    return arr

def build_symptom_vector(symptom_values: list[float]) -> np.ndarray:
    vec = np.array(symptom_values, dtype=np.float32)
    return np.expand_dims(vec, axis=0)  # (1,N)

def predict_keras(model, img_arr: np.ndarray, sym_vec: np.ndarray) -> np.ndarray:
    return model.predict([img_arr, sym_vec], verbose=0)[0]

def predict_tflite(interpreter, img_arr: np.ndarray, sym_vec: np.ndarray) -> np.ndarray:
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    def is_image(shape):
        return len(shape) == 4 and shape[1] == 224 and shape[2] == 224 and shape[3] == 3

    img_idx, sym_idx = None, None
    for d in input_details:
        shape = d["shape"]
        if is_image(shape):
            img_idx = d["index"]
        elif len(shape) == 2:
            sym_idx = d["index"]

    if img_idx is None or sym_idx is None:
        raise RuntimeError(f"Could not map TFLite inputs. Shapes: {[d['shape'] for d in input_details]}")

    img_dtype = next(d["dtype"] for d in input_details if d["index"] == img_idx)
    sym_dtype = next(d["dtype"] for d in input_details if d["index"] == sym_idx)

    interpreter.set_tensor(img_idx, img_arr.astype(img_dtype))
    interpreter.set_tensor(sym_idx, sym_vec.astype(sym_dtype))
    interpreter.invoke()

    out = interpreter.get_tensor(output_details[0]["index"])[0]
    return out

def sorted_probs(probs: np.ndarray):
    rows = [{"Class": c, "Probability": float(p)} for c, p in zip(CLASS_NAMES, probs)]
    rows.sort(key=lambda x: x["Probability"], reverse=True)
    return rows


# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("## 🧠 Cattle Disease AI")
    st.caption("Multimodal Fusion Demo (Image + Symptoms)")
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    page = st.radio("Navigation", ["Predict", "Model Info", "Deployment Notes"], index=0)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")
    use_tflite = st.toggle("Use TFLite inference", value=DEFAULT_USE_TFLITE)
    st.caption("Use Keras for server/API; TFLite for mobile/edge.")

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("### 📦 Paths")
    st.code(MODEL_PATH, language="text")
    st.code(TFLITE_PATH, language="text")


# ----------------------------
# HEADER
# ----------------------------
io = None
try:
    io = get_model_io_info()
except Exception as e:
    st.error(f"Model load failed: {e}")
    st.stop()

sym_dim = io["symptom_dim"]
out_dim = io["output_dim"]

# Validate CLASS_NAMES length
if len(CLASS_NAMES) != out_dim:
    st.error(f"CLASS_NAMES has {len(CLASS_NAMES)} items but model outputs {out_dim} classes. Fix CLASS_NAMES.")
    st.stop()

# Create symptom labels to match exact model dim
if len(SYMPTOM_LABELS) != sym_dim:
    SYMPTOM_LABELS = [f"Symptom {i+1}" for i in range(sym_dim)]

colA, colB = st.columns([0.7, 0.3], vertical_alignment="center")
with colA:
    st.markdown("# 🐄 Cattle Disease Predictor")
    st.markdown(
        "<span class='muted'>Upload a cattle image and select symptoms to predict "
        "<b>Normal</b>, <b>LSD</b>, or <b>FMD</b>.</span>",
        unsafe_allow_html=True,
    )
with colB:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Status**  \n<span class='badge'>Demo-ready</span>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown(
        f"**Inputs**: Image + {sym_dim} Symptoms  \n"
        f"**Output classes**: {out_dim}  \n"
        f"**Model**: MobileNetV2 + MLP Fusion",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")


# ----------------------------
# PAGES
# ----------------------------
if page == "Predict":
    left, right = st.columns([0.55, 0.45], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 1) Upload Image")
        st.markdown('<span class="muted">Supported: JPG/PNG</span>', unsafe_allow_html=True)
        uploaded = st.file_uploader(" ", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 2) Select Symptoms")
        st.markdown(
            "<span class='muted'>Checkboxes generate the symptom vector in the exact shape your model expects.</span>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        symptom_values = []
        cols = st.columns(2)
        for i, name in enumerate(SYMPTOM_LABELS):
            with cols[i % 2]:
                checked = st.checkbox(name, value=False, key=f"sym_{i}")
                symptom_values.append(1.0 if checked else 0.0)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        predict = st.button("🔎 Predict", type="primary", use_container_width=True, disabled=(uploaded is None))

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Results")
        st.markdown('<span class="muted">Prediction + probability distribution.</span>', unsafe_allow_html=True)
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        if uploaded is None:
            st.info("Upload an image on the left, then click **Predict**.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            pil_img = Image.open(uploaded)
            st.image(pil_img, caption="Uploaded image", use_column_width=True)

            if predict:
                try:
                    img_arr = preprocess_image(pil_img)
                    sym_vec = build_symptom_vector(symptom_values)

                    if use_tflite:
                        interpreter = load_tflite_interpreter(TFLITE_PATH)
                        probs = predict_tflite(interpreter, img_arr, sym_vec)
                        model_type = "TFLite"
                    else:
                        model = load_keras_model(MODEL_PATH)
                        probs = predict_keras(model, img_arr, sym_vec)
                        model_type = "Keras"

                    probs = np.array(probs, dtype=np.float32)
                    pred_idx = int(np.argmax(probs))
                    pred_label = CLASS_NAMES[pred_idx]
                    conf = float(probs[pred_idx])

                    # Metrics row
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Prediction", pred_label)
                    m2.metric("Confidence", f"{conf:.2%}")
                    m3.metric("Inference", model_type)

                    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

                    st.markdown("#### Probability Distribution")
                    for row in sorted_probs(probs):
                        st.write(f"**{row['Class']}** — {row['Probability']:.3f}")
                        st.progress(min(max(row["Probability"], 0.0), 1.0))

                    with st.expander("Show exact probabilities"):
                        st.table(sorted_probs(probs))

                    with st.expander("Show symptom vector used"):
                        st.write({"symptom_dim": sym_dim, "vector": symptom_values})

                except Exception as e:
                    st.error(f"Prediction failed: {e}")

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Click **Predict** to run inference.")
                st.markdown("</div>", unsafe_allow_html=True)


elif page == "Model Info":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Model I/O Information")
    st.write("Detected from your saved model file:")
    st.json(io)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("### Notes")
    st.write(
        "- If you want real symptom names, update `SYMPTOM_LABELS` to match your training feature order.\n"
        "- If you trained with 8 symptoms, the UI will automatically use 8 inputs and avoid shape mismatch."
    )
    st.markdown("</div>", unsafe_allow_html=True)


elif page == "Deployment Notes":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Deployment plan (MVP-ready)")
    st.write(
        "**Option A: FastAPI + Swagger UI (Supervisor-friendly)**\n"
        "- Load `fusion_model.keras`\n"
        "- Endpoint `/predict` accepts: image + symptom vector\n"
        "- Test using Swagger UI / Postman\n\n"
        "**Option B: Mobile/Edge**\n"
        "- Use `fusion_model.tflite`\n"
        "- Keep MobileNetV2 preprocessing identical to training"
    )
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("### Important alignment checks")
    st.write(
        "- `CLASS_NAMES` must match your model output order.\n"
        "- Symptoms must be in the same order as training. This app matches dimension automatically."
    )
    st.markdown("</div>", unsafe_allow_html=True)