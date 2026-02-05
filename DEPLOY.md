# Cattle Disease AI API

A FastAPI-based REST API for cattle health prediction using TensorFlow Lite models.

## Features

- ✅ Fast and efficient predictions using TFLite
- ✅ RESTful API endpoints
- ✅ CORS support for cross-origin requests
- ✅ Automatic API documentation (interactive Swagger UI)
- ✅ Health check endpoints
- ✅ Ready for Render deployment

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Cattle_disease-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

## API Endpoints

### 1. Health Check
**GET** `/`

Response:
```json
{
  "status": "healthy",
  "service": "Cattle Disease AI API",
  "version": "1.0.0"
}
```

### 2. Detailed Health Status
**GET** `/health`

Response:
```json
{
  "status": "ok",
  "model_loaded": true,
  "api_version": "1.0.0"
}
```

### 3. Make Prediction
**POST** `/predict`

Request:
```json
{
  "features": [1.0, 2.0, 3.0, 4.0, 5.0]
}
```

Response:
```json
{
  "prediction": 0.73,
  "confidence": 0.46,
  "class_label": "Diseased"
}
```

### 4. Model Information
**GET** `/model-info`

Response:
```json
{
  "model_path": "/path/to/cattle_health_mvp.tflite",
  "input_shape": [1, 5],
  "input_dtype": "<dtype: 'float32'>",
  "output_shape": [1, 1],
  "output_dtype": "<dtype: 'float32'>"
}
```

## Deployment on Render

### Option 1: Using Git Integration (Recommended)

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Add FastAPI for cattle disease prediction"
git push origin main
```

2. **Create a new Web Service on Render**:
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Choose branch (main)

3. **Configure the service**:
   - **Name**: cattle-disease-api
   - **Environment**: Python 3
   - **Region**: Choose closest to your location
   - **Plan**: Free (or higher for better performance)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables** (if needed):
   - Add any required environment variables in the Render dashboard

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy

### Option 2: Using render.yaml

1. Push your code to GitHub with the `render.yaml` file
2. On Render, select "Infrastructure as Code"
3. Connect your repository
4. Render will automatically detect and deploy using the `render.yaml` configuration

## Environment Variables

The API reads the following environment variables:

- `PORT` - Server port (default: 8000)

## Model Details

The API expects:
- **Input**: Feature vector matching your TFLite model's input shape
- **Output**: Prediction score (continuous value from 0-1)

The default implementation assumes:
- Input shape: [1, n_features]
- Output shape: [1, 1]
- Threshold for classification: 0.5 (< 0.5 = Healthy, >= 0.5 = Diseased)

Adjust these values in `app.py` based on your specific model requirements.

## Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/

# Get model info
curl http://localhost:8000/model-info

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0, 5.0]}'
```

## Troubleshooting

### Model not loading
- Ensure the TFLite model file exists at `ml/model/cattle_health_mvp.tflite`
- Check file permissions
- Verify model format is valid

### Prediction errors
- Ensure input features match the model's expected input shape
- Check data types are correct (should be float)
- Verify feature normalization/scaling if required by the model

### Port issues on Render
- Render automatically sets the `$PORT` environment variable
- The start command must use `$PORT` not a hardcoded port

## Performance Tips

- ✅ TFLite is very efficient for mobile and edge deployments
- ✅ Use Render's paid plans for better performance if needed
- ✅ Consider using a database for logging predictions
- ✅ Implement caching for repeated requests

## License

[Add your license here]

## Support

For issues or questions, please open an issue in the repository.
