# 💼 AI Resume Analyzer

AI Resume Analyzer is an intelligent, professional web application designed to help candidates optimize their resumes for Applicant Tracking Systems (ATS) and specific job descriptions. Powered by advanced AI (Groq API), this tool provides actionable feedback, strategic insights, and tailored interview questions to enhance career opportunities.

## ✨ Features

- **Document Parsing**: Seamlessly extract text from PDF and DOCX resume files.
- **AI-Powered Analysis**: Generates a detailed "Role Alignment Score" and ATS compatibility percentage based on the provided job description.
- **Strategic Insights & Feedback**: Identifies missing skills, proposes optimization opportunities, and offers refined bullet points for maximum impact.
- **Interview Preparation**: Synthesizes custom behavioral and technical interview questions based on the candidate's active profile and job context.
- **History Dashboard**: Automatically saves processed documents to a built-in database to track progress and past scores.
- **Modern UI/UX**: Clean, professional interface built with Streamlit and Plotly for interactive data visualization.

## 🛠️ Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/)
- **Backend**: Python
- **AI Engine**: [Groq API](https://groq.com/)
- **Document Processing**: `PyPDF2`, `python-docx`
- **Database**: SQLite (Mocked as MongoDB collections)

## 🚀 Setup Instructions

Follow these steps to run the application locally:

### 1. Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com/keys)

### 2. Clone the Repository
```bash
git clone https://github.com/shivasync0/Resume-Analyzer.git
cd Resume-Analyzer
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application
Start the Streamlit application:
```bash
streamlit run app.py
```
*The app will automatically open in your default browser at `http://localhost:8501`.*
