# Cattle Disease AI

## Description
Hybrid online-offline explainable ML system for early detection of priority cattle diseases using images and clinical symptoms. The solution includes a FastAPI backend, Grad-CAM explainability, and a deployment on Render.

## GitHub Repository
- https://github.com/nmaketh/Cattle_disease-ai

## Setup
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

## Designs (Mockups / Screens)
- Streamlit UI screenshot: [designs/screenshots/streamlit.png](designs/screenshots/streamlit.png)
- Streamlit UI run: `streamlit run streamlit_app.py`
- Streamlit app URL: https://cattledisease-ai-drzbcmhavbpzqiz2bnvjkt.streamlit.app/
- Swagger UI screenshot: [designs/screenshots/swagger%20UI.png](designs/screenshots/swagger%20UI.png)
- /predict response screenshot: [designs/screenshots/predict-response.png](designs/screenshots/predict-response.png)
- Grad-CAM sample heatmap: [designs/screenshots/grad-Cam.png](designs/screenshots/grad-Cam.png)

Note: The Streamlit UI sends optional symptom inputs to the API. If no symptoms are selected, a zero vector is sent.

## Deployment Plan
- Platform: Render
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Live URL: https://cattle-disease-ai.onrender.com

## Video Demo
- Demo video: TODO add link

## Code Files
- API: [app.py](app.py)
- Notebook: [ml/model/Nhial_Majok_ML_Track_Final%20(3).ipynb](ml/model/Nhial_Majok_ML_Track_Final%20(3).ipynb)
- Tests: [test_api.py](test_api.py)