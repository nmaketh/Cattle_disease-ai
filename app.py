import os
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Cattle Disease AI API",
    description="ML API for cattle health prediction",
    version="1.0.0"
)

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

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading model: {str(e)}")
    interpreter = None


class PredictionInput(BaseModel):
    """Input data for model prediction"""
    features: List[float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [1.0, 2.0, 3.0, 4.0, 5.0]
            }
        }


class PredictionOutput(BaseModel):
    """Output from model prediction"""
    prediction: float
    confidence: Optional[float] = None
    class_label: Optional[str] = None


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
        # Convert input to numpy array
        features = np.array(input_data.features, dtype=np.float32)
        
        # Reshape to match model input
        input_shape = input_details[0]['shape']
        features = features.reshape(input_shape)
        
        # Set input and run inference
        interpreter.set_tensor(input_details[0]['index'], features)
        interpreter.invoke()
        
        # Get output
        output_data = interpreter.get_tensor(output_details[0]['index'])
        prediction = float(output_data.flatten()[0])
        
        # Determine class label based on prediction threshold
        class_label = "Healthy" if prediction < 0.5 else "Diseased"
        
        return PredictionOutput(
            prediction=prediction,
            confidence=abs(prediction - 0.5) * 2,  # Simple confidence metric
            class_label=class_label
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if interpreter is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_path": MODEL_PATH,
        "input_shape": input_details[0]['shape'].tolist() if input_details else None,
        "input_dtype": str(input_details[0]['dtype']) if input_details else None,
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
