import base64
import binascii
import hashlib
import io
import logging
import os
from collections import OrderedDict
from threading import Lock

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PIL import Image
from typing import List, Optional, Union
import uvicorn

app = FastAPI(
    title="Cattle Disease AI API",
    description="ML API for cattle health prediction",
    version="1.0.0"
)

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("cattle_disease_api")

CACHE_MAX_ITEMS = int(os.getenv("CACHE_MAX_ITEMS", "256"))
HEATMAP_HEIGHT = int(os.getenv("HEATMAP_HEIGHT", "32"))
HEATMAP_SCALE_X = int(os.getenv("HEATMAP_SCALE_X", "16"))
HEATMAP_SCALE_Y = int(os.getenv("HEATMAP_SCALE_Y", "4"))
CLASS_NAMES = [
    "CBPP",
    "ECF",
    "FOOT-AND-MOUTH",
    "HEALTHY",
    "LSD"
]

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the TFLite model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "model", "cattle_health_mvp.tflite")
KERAS_MODEL_PATH = os.getenv(
    "KERAS_MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "ml", "model", "cattle_health_mvp.h5")
)

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading model: {str(e)}")
    interpreter = None

try:
    keras_model = tf.keras.models.load_model(KERAS_MODEL_PATH)
    keras_model.trainable = False
    print(f"✓ Keras model loaded successfully from {KERAS_MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading Keras model: {str(e)}")
    keras_model = None

INFERENCE_LOCK = Lock()


class LRUCache:
    def __init__(self, max_items: int):
        self.max_items = max_items
        self._data = OrderedDict()
        self._lock = Lock()

    def get(self, key):
        with self._lock:
            if key not in self._data:
                return None
            value = self._data.pop(key)
            self._data[key] = value
            return value

    def set(self, key, value):
        with self._lock:
            if key in self._data:
                self._data.pop(key)
            self._data[key] = value
            if len(self._data) > self.max_items:
                self._data.popitem(last=False)


PREDICTION_CACHE = LRUCache(CACHE_MAX_ITEMS)
EXPLAIN_CACHE = LRUCache(CACHE_MAX_ITEMS)


class PredictionInput(BaseModel):
    """Input data for model prediction"""
    image_base64: str = Field(..., description="Base64-encoded PNG/JPEG image")
    symptoms: Optional[List[float]] = Field(
        default=None,
        description="Optional symptom vector [fever, nodules, mouth_sores, nasal_discharge, cough, swollen_lymph]"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_base64": "iVBORw0KGgoAAA...",
                "symptoms": [1, 0, 1, 0, 0, 0]
            }
        }


class PredictionOutput(BaseModel):
    """Output from model prediction"""
    prediction: Union[float, List[float]]
    confidence: Optional[float] = None
    class_label: Optional[str] = None


class ExplainabilityOutput(BaseModel):
    """Explainability payload for feature-based heatmap"""
    heatmap_png_base64: str = Field(..., description="Base64-encoded PNG heatmap")
    method: str = Field(..., description="Explainability method used")
    normalization: str = Field(..., description="Normalization strategy used to build the heatmap")
    heatmap_shape: List[int] = Field(..., description="Height and width of the heatmap image")


class PredictionExplainOutput(PredictionOutput):
    """Prediction output with explainability"""
    explainability: ExplainabilityOutput


def _bytes_to_key(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()


def _get_image_input_detail():
    if not input_details:
        return None
    for detail in input_details:
        if len(detail.get("shape", [])) == 4:
            return detail
    return input_details[0]


def _get_symptom_input_detail():
    if not input_details:
        return None
    for detail in input_details:
        if len(detail.get("shape", [])) == 2:
            return detail
    return input_details[1] if len(input_details) > 1 else None


def _get_symptom_length(default_len: int = 6) -> int:
    try:
        if keras_model is not None and len(keras_model.inputs) > 1:
            return int(keras_model.inputs[1].shape[-1])
    except Exception:
        pass
    detail = _get_symptom_input_detail()
    if detail is not None:
        try:
            return int(detail.get("shape", [1, default_len])[-1])
        except Exception:
            return default_len
    return default_len


def _prepare_symptoms(symptoms: Optional[List[float]], expected_len: int) -> np.ndarray:
    if symptoms is None:
        values = np.zeros((expected_len,), dtype=np.float32)
    else:
        if len(symptoms) != expected_len:
            raise ValueError(f"symptoms must have length {expected_len}")
        values = np.asarray(symptoms, dtype=np.float32)
    return values.reshape(1, expected_len)


def _run_inference(features: np.ndarray, symptoms: Optional[List[float]] = None) -> PredictionOutput:
    with INFERENCE_LOCK:
        if not input_details:
            raise ValueError("Model input details unavailable")

        if len(input_details) == 1:
            interpreter.set_tensor(input_details[0]["index"], features)
        else:
            image_detail = _get_image_input_detail()
            symptom_detail = _get_symptom_input_detail()
            if image_detail is None:
                image_detail = input_details[0]
            interpreter.set_tensor(image_detail["index"], features)

            if symptom_detail is not None:
                expected_len = int(symptom_detail.get("shape", [1, 6])[-1])
                symptom_array = _prepare_symptoms(symptoms, expected_len)
                interpreter.set_tensor(symptom_detail["index"], symptom_array)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])

    flat = output_data.flatten().astype(np.float32)
    if flat.size == 1:
        prediction = float(flat[0])
        class_label = "Healthy" if prediction < 0.5 else "Diseased"
        return PredictionOutput(
            prediction=prediction,
            confidence=abs(prediction - 0.5) * 2,
            class_label=class_label
        )

    if np.all((flat >= 0.0) & (flat <= 1.0)) and abs(float(flat.sum()) - 1.0) < 1e-3:
        probs = flat
    else:
        logits = flat - float(flat.max())
        exp_vals = np.exp(logits)
        probs = exp_vals / exp_vals.sum()
    top_idx = int(np.argmax(probs))
    class_label = CLASS_NAMES[top_idx] if top_idx < len(CLASS_NAMES) else f"class_{top_idx}"
    return PredictionOutput(
        prediction=probs.tolist(),
        confidence=float(probs[top_idx]),
        class_label=class_label
    )


def _get_last_conv_layer(model: tf.keras.Model):
    for layer in reversed(model.layers):
        try:
            output_shape = layer.output_shape
        except Exception:
            output_shape = None
        if output_shape is not None and isinstance(output_shape, (list, tuple)):
            if len(output_shape) == 4:
                return layer
        if hasattr(layer, "output"):
            try:
                if len(layer.output.shape) == 4:
                    return layer
            except Exception:
                continue
    raise ValueError("No 4D convolutional layer found for Grad-CAM")


def _compute_gradcam(image_array: np.ndarray, class_index: int, symptoms_array: Optional[np.ndarray]) -> np.ndarray:
    if keras_model is None:
        raise ValueError("Keras model not available for Grad-CAM")

    conv_layer = _get_last_conv_layer(keras_model)
    grad_model = tf.keras.Model(
        [keras_model.inputs],
        [conv_layer.output, keras_model.output]
    )

    with tf.GradientTape() as tape:
        if len(keras_model.inputs) > 1:
            conv_outputs, predictions = grad_model([image_array, symptoms_array])
        else:
            conv_outputs, predictions = grad_model(image_array)
        if predictions.shape[-1] <= class_index:
            raise ValueError("Class index out of range for Grad-CAM")
        class_channel = predictions[:, class_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    max_val = tf.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val

    heatmap = tf.image.resize(heatmap[..., tf.newaxis], (image_array.shape[1], image_array.shape[2]))
    return heatmap[..., 0].numpy()


def _normalize_features(features: np.ndarray) -> np.ndarray:
    abs_vals = np.abs(features).astype(np.float32)
    max_val = float(abs_vals.max()) if abs_vals.size else 0.0
    if max_val == 0.0:
        return abs_vals
    return abs_vals / max_val


def _build_heatmap_png_base64(norm_values: np.ndarray) -> tuple[str, List[int]]:
    values = np.asarray(norm_values, dtype=np.float32)
    if values.size == 0:
        values = np.zeros((1,), dtype=np.float32)
    if values.ndim == 1:
        values = np.tile(values, (HEATMAP_HEIGHT, 1))
    img = (values * 255.0).clip(0, 255).astype(np.uint8)
    image = Image.fromarray(img, mode="L")
    image = image.resize(
        (max(1, image.size[0] * HEATMAP_SCALE_X), max(1, image.size[1] * HEATMAP_SCALE_Y)),
        resample=Image.NEAREST
    )
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return encoded, [image.size[1], image.size[0]]


def _decode_image(image_base64: str) -> tuple[np.ndarray, bytes, np.ndarray]:
    try:
        image_bytes = base64.b64decode(image_base64)
    except binascii.Error as exc:
        raise ValueError("Invalid base64 image data") from exc

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise ValueError("Invalid image data") from exc
    image_detail = _get_image_input_detail()
    if image_detail is None:
        raise ValueError("Model input details unavailable")
    input_shape = image_detail["shape"]
    if len(input_shape) != 4:
        raise ValueError("Model input must be 4D (batch, height, width, channels)")
    height, width = int(input_shape[1]), int(input_shape[2])
    resized = image.resize((width, height), resample=Image.BILINEAR)
    array = np.asarray(resized, dtype=np.float32) / 255.0
    array = np.expand_dims(array, axis=0)
    return array, image_bytes, np.asarray(resized, dtype=np.float32)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Cattle Disease AI API",
        "version": "1.0.0"
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Make a prediction using the cattle health model
    
    Args:
        input_data: Feature vector for prediction
        
    Returns:
        Prediction output with confidence score
    """
    if interpreter is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        features, image_bytes, _ = _decode_image(input_data.image_base64)

        cache_key = _bytes_to_key(image_bytes)
        cached = PREDICTION_CACHE.get(cache_key)
        if cached is not None:
            return cached

        result = _run_inference(features, input_data.symptoms)
        PREDICTION_CACHE.set(cache_key, result)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-explain", response_model=PredictionExplainOutput)
async def predict_explain(input_data: PredictionInput):
    """
    Make a prediction and return a feature-based heatmap for explainability.

    Note: If the Keras model is unavailable or Grad-CAM fails, a fallback intensity heatmap is used.
    """
    if interpreter is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        features, image_bytes, resized = _decode_image(input_data.image_base64)

        cache_key = _bytes_to_key(image_bytes)
        cached = EXPLAIN_CACHE.get(cache_key)
        if cached is not None:
            return cached

        prediction_output = _run_inference(features, input_data.symptoms)
        top_class = 0
        if isinstance(prediction_output.prediction, list):
            top_class = int(np.argmax(np.array(prediction_output.prediction)))

        heatmap_method = "input-intensity"
        heatmap_values = None
        if keras_model is not None:
            try:
                symptom_len = _get_symptom_length()
                symptom_array = _prepare_symptoms(input_data.symptoms, symptom_len)
                heatmap_values = _compute_gradcam(features, top_class, symptom_array)
                heatmap_method = "grad-cam"
            except Exception as exc:
                logger.exception("Grad-CAM failed, falling back to intensity heatmap: %s", exc)
                heatmap_values = None

        if heatmap_values is None:
            grayscale = resized.mean(axis=2)
            heatmap_values = _normalize_features(grayscale)

        heatmap_b64, heatmap_shape = _build_heatmap_png_base64(heatmap_values)

        response = PredictionExplainOutput(
            prediction=prediction_output.prediction,
            confidence=prediction_output.confidence,
            class_label=prediction_output.class_label,
            explainability=ExplainabilityOutput(
                heatmap_png_base64=heatmap_b64,
                method=heatmap_method,
                normalization="abs-max",
                heatmap_shape=heatmap_shape
            )
        )
        EXPLAIN_CACHE.set(cache_key, response)
        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explainability error: {str(e)}")


@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if interpreter is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    input_shapes = [detail["shape"].tolist() for detail in input_details] if input_details else None
    input_dtypes = [str(detail["dtype"]) for detail in input_details] if input_details else None

    return {
        "model_path": MODEL_PATH,
        "keras_model_path": KERAS_MODEL_PATH,
        "keras_model_loaded": keras_model is not None,
        "input_shape": input_details[0]['shape'].tolist() if input_details else None,
        "input_dtype": str(input_details[0]['dtype']) if input_details else None,
        "input_shapes": input_shapes,
        "input_dtypes": input_dtypes,
        "output_shape": output_details[0]['shape'].tolist() if output_details else None,
        "output_dtype": str(output_details[0]['dtype']) if output_details else None,
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "model_loaded": interpreter is not None,
        "api_version": "1.0.0"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
