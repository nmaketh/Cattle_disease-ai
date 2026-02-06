# Cattle Disease AI

## Overview
Hybrid online-offline explainable ML system for early detection of priority cattle diseases using images and clinical symptoms. The solution includes a FastAPI backend, Grad-CAM explainability, and a deployment on Render.

## Repository
- https://github.com/nmaketh/Cattle_disease-ai

## Quickstart
1. Create a virtual environment:
	- `python -m venv venv`
	- `source venv/bin/activate`
2. Install dependencies:
	- `pip install -r requirements.txt`
3. Run the API:
	- `python app.py`
4. Open Swagger UI:
	- http://localhost:8000/docs
5. Run the Streamlit UI (mockup):
	- `streamlit run streamlit_app.py`
	- Optional: set `API_BASE_URL` to point at the API (default: https://cattle-disease-ai.onrender.com)

## Key Files
- Model notebook: [ml/Nhial_Majok_ML_Track_Final.ipynb](ml/Nhial_Majok_ML_Track_Final.ipynb)
- API server: [app.py](app.py)
- Streamlit UI: [streamlit_app.py](streamlit_app.py)
- Tests: [test_api.py](test_api.py)

## API
- Base URL (local): http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Live API URL: https://cattle-disease-ai.onrender.com

## Streamlit UI
- App URL: https://cattledisease-ai-drzbcmhavbpzqiz2bnvjkt.streamlit.app/
- Note: The UI sends optional symptom inputs to the API. If no symptoms are selected, a zero vector is sent.

## Designs (Mockups / Screens)
- Figma design file: https://www.figma.com/make/Pe0LgxsTbWJlefBGjsJrFb/Community-Animal-Health-App?t=yQnNg7tERaAAOYJj-1
- Streamlit UI screenshot: [designs/screenshots/streamlit.png](designs/screenshots/streamlit.png)
- Swagger UI screenshot: [designs/screenshots/swagger%20UI.png](designs/screenshots/swagger%20UI.png)
- /predict response screenshot: [designs/screenshots/prediction-response.png](designs/screenshots/prediction-response.png)

## Deployment
- Platform: Render
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Video Demo
- Demo video: https://drive.google.com/file/d/18AnR8wdVJF7xwExxxQ7Aj9vrNKsbCpW1/view?usp=sharing

## Submission Checklist
- README with description, setup, and deployment plan
- Repo link and code files
- Designs/screenshots
- Model notebook with data visualization, architecture, and metrics
- Video demo link (5 to 10 minutes)
