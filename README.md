# Cattle Disease AI

## Overview
This project delivers an initial MVP for cattle disease classification using a multimodal ML approach:
- **Image input** (cattle skin photos)
- **Optional symptom vector** (clinical observations)

**MVP classes supported:** **Normal**, **LSD (Lumpy Skin Disease)**, **FMD (Foot-and-Mouth Disease)**.

The solution includes:
- A **FastAPI backend** (Swagger UI for testing)
- A **Streamlit MVP UI** for end-user demonstration
- A **model notebook** documenting data engineering, model architecture, and performance metrics
- Deployment on **Render** (API) and **Streamlit Cloud** (UI)

## Repository
- https://github.com/nmaketh/Cattle_disease-ai


## MVP Scope vs Roadmap
### MVP (this submission)
-  Image + symptoms fusion model for: **Normal / LSD / FMD**
-  End-to-end demo via Streamlit + FastAPI
-  Model evaluation: accuracy, precision, recall, F1, confusion matrix
-  Deployment-ready artifacts and reproducible setup

### Roadmap (future phase)
-  Extend to additional diseases such as **ECF** and **CBPP** once reliable labeled datasets are available.
  These diseases are often **symptom-dominant** and require structured clinical data collection during pilot testing.


## Quickstart (Local)
1. Create and activate a virtual environment:
   - `python -m venv .venv`
   - `source .venv/bin/activate`

2. Install dependencies:
   - `python -m pip install -r requirements.txt`

3. Run the API:
   - `uvicorn app:app --host 0.0.0.0 --port 8000`

4. Open Swagger UI:
   - http://localhost:8000/docs

5. Run the Streamlit UI:
   - `python -m streamlit run streamlit_app.py`
   - Optional: set `API_BASE_URL` to point at the API (default: https://cattle-disease-ai.onrender.com)


## Key Files
- Model notebook: `ml/Nhial_Majok_ML_Track_Final.ipynb`
- API server: `app.py`
- Streamlit UI: `streamlit_app.py`
- Tests: `test_api.py`



## API
- Base URL (local): http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Live API URL: https://cattle-disease-ai.onrender.com

### Example Endpoints
- `POST /predict` (image + optional symptoms)
- `GET /model-info`
- `GET /health`


## Streamlit UI
- App URL: https://cattledisease-ai-drzbcmhavbpzqiz2bnvjkt.streamlit.app/
- The UI sends optional symptom inputs to the API. If no symptoms are selected, a zero vector is sent.


## Designs (Mockups / Screens)
- Figma design file: https://utter-offset-88332261.figma.site/
- Streamlit UI screenshot: `designs/screenshots/streamlit.png`
- Swagger UI screenshot: `designs/screenshots/swagger UI.png`
- /predict response screenshot: `designs/screenshots/prediction-response.png`


## Deployment
### API (Render)
- Platform: Render
- Start command:
  - `uvicorn app:app --host 0.0.0.0 --port $PORT`

### UI (Streamlit Cloud)
- Platform: Streamlit Community Cloud
- Entry: `streamlit_app.py`


## Video Demo
- Demo video: https://drive.google.com/file/d/1EunB42bvMj6tvBSwFUt71Rs8pjR9bFKj/view?usp=sharing


## Submission Checklist
-  README with description, setup, and deployment plan
-  Repo link and code files
-  Designs/screenshots
-  Model notebook with data visualization, architecture, and metrics
-  Video demo link (5–10 minutes)
