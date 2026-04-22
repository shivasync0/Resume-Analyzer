# AI Resume Analyzer Pro (Python) - Setup Instructions

Everything is now built using a pure Python stack for maximum performance and AI flexibility.

## Prerequisites
- Python 3.9+
- MongoDB (running locally or a cloud URI)
- Google Gemini API Key

## Backend Setup (FastAPI)
1. Open a terminal in the `backend` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `backend/.env` with your `GEMINI_API_KEY`.
4. Run the API:
   ```bash
   python main.py
   ```
   *The API will be available at `http://localhost:8000`. You can see the documentation at `/docs`.*

## Frontend Setup (Streamlit)
1. Open a new terminal in the `frontend` folder.
2. Run the UI:
   ```bash
   streamlit run app.py
   ```
   *The UI will open automatically in your browser at `http://localhost:8501`.*

## Key Python Libraries Used
- **FastAPI**: Modern, high-performance web framework.
- **Streamlit**: Interactive UI for AI and Data apps.
- **Motor**: Asynchronous MongoDB driver.
- **Google Generative AI**: SDK for Gemini 1.5 Flash.
- **PyPDF2 & python-docx**: Robust file parsing.
- **Plotly**: Premium interactive data visualizations.
