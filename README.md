# ✨ AI Resume Analyzer Pro

An intelligent and professional Resume Analyzer built using Python and Streamlit.
This tool helps users upload resumes and get quick AI-driven insights such as keyword matching, resume scoring, skills extraction, and personalized feedback for improving job applications.

---

## 🚀 Features

- **Upload Resume**: Supports PDF and DOCX formats.
- **AI-Powered Analysis**: Extracts text and analyzes resume content using Groq AI models.
- **Scoring System**: Generates an ATS compatibility and overall resume score.
- **Skill Extraction & Matching**: Identifies missing skills based on the target job description.
- **Suggestions for Improvement**: Provides actionable feedback to optimize bullets and content.
- **Interview Prep**: Synthesizes behavioral and technical questions based on the candidate's profile.
- **Modern UI**: Clean, premium, and interactive interface built with Streamlit and Plotly.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, SQLite
- **AI Engine**: Groq API (`gemma2-9b-it`)
- **Libraries**:
  - `python-docx` / `PyPDF2` for text extraction
  - `plotly` for data visualization
  - `pandas` for dashboard data management
  - `scikit-learn` / `pymongo` (dependencies)

---

## 💻 Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Resume-Analyzer.git
   cd Resume-Analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## 💡 How It Works

1. **User uploads a resume** and pastes a target job description.
2. **System extracts text** from the provided file.
3. **AI models analyze** the text to map skills, experience, and structure.
4. **Resume is compared** against the job description to calculate an alignment score.
5. **Dashboard presents insights**, improvements, and generated interview questions.
