import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #0ea5e9;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def dashboard():
    st.title("🚀 AI Resume Analyzer Pro 👋")
    st.markdown("### Land your dream job with AI-powered insights.")
    
    tabs = st.tabs(["Analyze Resume", "History", "Interview Prep"])
    
    with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Upload Resume")
            uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
            job_desc = st.text_area("Job Description (Optional)", placeholder="Paste JD here for better matching...")
            
            if st.button("Start AI Analysis"):
                if uploaded_file:
                    with st.spinner("AI is analyzing your resume..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        res = requests.post(f"{API_URL}/analyze", files=files, data={"job_description": job_desc})
                        if res.status_code == 200:
                            st.session_state.analysis = res.json()
                            st.success("Analysis complete!")
                        else:
                            st.error("Analysis failed")
                else:
                    st.warning("Please upload a file first")

        if 'analysis' in st.session_state:
            data = st.session_state.analysis
            with col2:
                st.subheader("Analysis Summary")
                score = data['analysis']['score']
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': "Match Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#0ea5e9"},
                        'steps': [
                            {'range': [0, 50], 'color': "#fee2e2"},
                            {'range': [50, 80], 'color': "#fef3c7"},
                            {'range': [80, 100], 'color': "#dcfce7"}
                        ]
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)

            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info("💡 **Feedback**")
                st.write(data['analysis']['feedback']['general'])
            with c2:
                st.warning("⚠️ **Missing Skills**")
                for skill in data['analysis']['missing_skills']:
                    st.markdown(f"- {skill}")
            with c3:
                st.success("🎯 **Suggestions**")
                for sug in data['analysis']['improvement_suggestions']:
                    st.markdown(f"- {sug}")

            st.subheader("AI Rewritten Bullets")
            for bullet in data['analysis']['rewritten_bullets']:
                with st.expander(f"Improvement for: {bullet['original'][:50]}..."):
                    st.markdown(f"**Original:** {bullet['original']}")
                    st.markdown(f"**Suggested:** :green[{bullet['suggested']}]")

    with tabs[1]:
        st.subheader("Recent Analysis History")
        res = requests.get(f"{API_URL}/history")
        if res.status_code == 200:
            history = res.json()
            if history:
                df = pd.DataFrame([
                    {
                        "Filename": h['filename'], 
                        "Score": h['analysis']['score'], 
                        "Date": h.get('date', 'Recent')
                    } for h in history
                ])
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No history found.")

    with tabs[2]:
        st.subheader("AI Interview Coach")
        if 'analysis' in st.session_state:
            if st.button("Generate Interview Questions"):
                res = requests.get(f"{API_URL}/questions/{st.session_state.analysis['_id']}")
                if res.status_code == 200:
                    questions = res.json()['questions']
                    for i, q in enumerate(questions):
                        st.markdown(f"**Q{i+1}:** {q}")
                else:
                    st.error("Failed to generate questions")
        else:
            st.info("Analyze a resume first to generate tailored questions.")

# Start Dashboard
if __name__ == "__main__":
    dashboard()
