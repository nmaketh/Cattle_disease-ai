# Quick Start: Deploy to Render

## Step 1: Prepare Your GitHub Repository

Make sure all files are committed:
```bash
git add .
git commit -m "Add FastAPI for cattle disease prediction"
git push origin main
```

## Step 2: Create Account on Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your repositories

## Step 3: Deploy the Service

### Option A: Quick Deploy (Recommended)

1. Go to Render Dashboard
2. Click **"New +"** button
3. Select **"Web Service"**
4. Select your GitHub repository
5. Enter:
   - **Name**: `cattle-disease-api`
   - **Root Directory**: `/` (if repo root) or path to the app
   - **Environment**: Select `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Select your preferred plan (free tier available)
7. Click **"Create Web Service"**

### Option B: Deploy Using render.yaml

Your `render.yaml` is already configured. Just:

1. Go to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Select your GitHub repository
4. Render will automatically read `render.yaml`
5. Click **"Deploy"**

## Step 4: Monitor Deployment

1. Watch the deployment logs in real-time
2. Wait for "Live" status (usually 2-5 minutes)
3. Click the generated URL to access your API

## Step 5: Test Your API

Once deployed, test with:

```bash
# Get the deployed URL from Render (e.g., https://cattle-disease-api.onrender.com)

# Health check
curl https://your-api.onrender.com/

# Interactive API docs
# Go to: https://your-api.onrender.com/docs

# Make prediction
curl -X POST https://your-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0, 5.0]}'
```

## Step 6: Configure Environment Variables (Optional)

If you need environment variables:

1. Go to your service on Render
2. Click **"Settings"** → **"Environment"**
3. Add variables as needed
4. Service will automatically restart

## Troubleshooting

### Service keeps failing to deploy

**Error: "ModuleNotFoundError"**
- Ensure all packages are in `requirements.txt`
- Check Python version is 3.11 in render.yaml

**Error: "Model not found"**
- Verify TFLite file is committed to git
- Check file path in `app.py` matches your repo structure
- Use relative paths (not absolute)

### Slow predictions

- This is expected on free tier (shared resources)
- Upgrade to paid plan for better performance
- Consider model optimization/quantization

### 502 Bad Gateway

- Check logs in Render dashboard
- Ensure start command is correct
- Verify model loads successfully

### High memory usage

- TFLite models are lightweight
- If still high, check for memory leaks
- Restart the service from Render dashboard

## Useful Links

- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow Lite Guide](https://www.tensorflow.org/lite)

## Next Steps

- Add database for logging predictions
- Implement authentication if needed
- Set up monitoring and alerts
- Add more prediction endpoints for different cattle metrics
- Consider horizontal scaling on paid plans

---

**Your API is now live! 🎉**
