"""
Example client script to test the Cattle Disease AI API
"""

import requests
import json

# API endpoint (change to your deployed URL)
API_URL = "http://localhost:8000"

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
    
    # Example features (adjust based on your model input)
    test_data = {
        "features": [1.0, 2.0, 3.0, 4.0, 5.0]
    }
    
    response = requests.post(
        f"{API_URL}/predict",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_batch_prediction():
    """Test multiple predictions"""
    print("Testing batch predictions...")
    
    test_cases = [
        {"features": [0.5, 1.0, 1.5, 2.0, 2.5]},
        {"features": [2.0, 2.0, 2.0, 2.0, 2.0]},
        {"features": [5.0, 4.5, 4.0, 3.5, 3.0]},
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
        test_batch_prediction()
        
        print("=" * 50)
        print("✓ All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the API")
        print(f"  Make sure the API is running at {API_URL}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
