"""
Example client script to test the Cattle Disease AI API
"""

import base64
import json
from pathlib import Path

import requests

# API endpoint (change to your deployed URL)
API_URL = "http://localhost:8000"
SAMPLE_IMAGE_PATH = Path("designs") / "sample_image.png"


def _load_sample_image_base64() -> str:
    image_bytes = SAMPLE_IMAGE_PATH.read_bytes()
    return base64.b64encode(image_bytes).decode("ascii")

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_root():
    """Test the root endpoint"""
    print("Testing / endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_model_info():
    """Test the model info endpoint"""
    print("Testing /model-info endpoint...")
    response = requests.get(f"{API_URL}/model-info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_prediction():
    """Test the prediction endpoint"""
    print("Testing /predict endpoint...")
    
    test_data = {
        "image_base64": _load_sample_image_base64()
    }
    
    response = requests.post(
        f"{API_URL}/predict",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_prediction_explain():
    """Test prediction with explainability endpoint"""
    print("Testing /predict-explain endpoint...")

    test_data = {
        "image_base64": _load_sample_image_base64()
    }

    response = requests.post(
        f"{API_URL}/predict-explain",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )

    payload = response.json()
    if "explainability" in payload:
        heatmap_len = len(payload["explainability"].get("heatmap_png_base64", ""))
        payload["explainability"]["heatmap_png_base64"] = f"<base64 length={heatmap_len}>"

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(payload, indent=2)}\n")

def test_batch_prediction():
    """Test multiple predictions"""
    print("Testing batch predictions...")
    
    test_cases = [
        {"image_base64": _load_sample_image_base64()},
        {"image_base64": _load_sample_image_base64()},
        {"image_base64": _load_sample_image_base64()},
    ]
    
    for i, test_data in enumerate(test_cases):
        print(f"Prediction {i+1}:")
        response = requests.post(
            f"{API_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("Cattle Disease AI API Test Suite")
    print("=" * 50 + "\n")
    
    try:
        test_root()
        test_health()
        test_model_info()
        test_prediction()
        test_prediction_explain()
        test_batch_prediction()
        
        print("=" * 50)
        print("✓ All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the API")
        print(f"  Make sure the API is running at {API_URL}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
