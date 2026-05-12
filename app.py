import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.parser import extract_text
from backend.ai_engine import analyze_resume, generate_questions
from backend.database import resumes_collection

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional White UI Design Custom CSS
st.markdown("""
    <style>
    /* Clean white background and minimalist text */
    .stApp {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 600;
        color: #111827;
        letter-spacing: -0.025em;
    }
    
    /* Subtle container styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
        border-radius: 0px;
        color: #6b7280;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0f172a;
        border-bottom-color: #0f172a;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
        color: #0f172a;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        border-color: #0f172a;
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Primary action button styling if needed */
    .primary-btn>button {
        background-color: #0f172a;
        color: #ffffff;
        border: none;
    }
    .primary-btn>button:hover {
        background-color: #1e293b;
        color: #ffffff;
    }
    
    /* Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #0f172a;
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 6px;
        border: 1px solid #cbd5e1;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #0f172a;
        box-shadow: 0 0 0 1px #0f172a;
    }
    
    /* Alerts/Messages */
    .stSuccess {
        background-color: #f0fdf4;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    .stError {
        background-color: #fef2f2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }
    .stWarning {
        background-color: #fffbeb;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .stInfo {
        background-color: #f0f9ff;
        color: #075985;
        border: 1px solid #bae6fd;
    }
    
    /* File uploader */
    div[data-testid="stFileUploadDropzone"] {
        background-color: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 8px;
    }
    div[data-testid="stFileUploadDropzone"]:hover {
        background-color: #f1f5f9;
        border-color: #94a3b8;
    }
    </style>
""", unsafe_allow_html=True)

def dashboard():
    # Header
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem; font-weight: 700;'>Intelligent Resume Analytics</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Analysis", "Dashboard", "Interview Prep"])
    
    with tabs[0]:
        col1, col2 = st.columns([5, 7], gap="large")
        
        with col1:
            st.markdown("### Document Upload")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem;'>Upload a candidate's resume (PDF/DOCX) for AI-driven insights.</p>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx"], label_visibility="collapsed")
            
            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown("### Target Role Context")
            job_desc = st.text_area("Job Description", placeholder="Paste job description here to tailor the analysis...", height=150, label_visibility="collapsed")
            
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("Generate Analysis Report", use_container_width=True):
                if uploaded_file:
                    with st.spinner("Processing document..."):
                        try:
                            raw_text = extract_text(uploaded_file.getvalue(), uploaded_file.name)
                            analysis_result = analyze_resume(raw_text, job_desc)
                            
                            resume_doc = {
                                "user_email": "guest@example.com",
                                "filename": uploaded_file.name,
                                "raw_text": raw_text,
                                "job_description": job_desc,
                                "parsed_data": analysis_result.get("parsedData", {}),
                                "analysis": analysis_result.get("analysis", {})
                            }
                            
                            inserted = resumes_collection.insert_one(resume_doc)
                            resume_doc["_id"] = str(inserted.inserted_id)
                            st.session_state.analysis = resume_doc
                            st.session_state.questions = None # Reset questions for new analysis
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
                else:
                    st.warning("Please provide a document to proceed.")

        with col2:
            if 'analysis' in st.session_state:
                data = st.session_state.analysis
                analysis_data = data.get('analysis', {})
                parsed_data = data.get('parsed_data', {})
                
                st.markdown("### Executive Summary")
                
                score = analysis_data.get('score', 0)
                
                # Professional gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': "Role Alignment Score", 'font': {'size': 16, 'color': '#64748b'}},
                    number = {'font': {'size': 48, 'color': '#0f172a'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                        'bar': {'color': "#0f172a"},
                        'bgcolor': "white",
                        'borderwidth': 0,
                        'steps': [
                            {'range': [0, 50], 'color': "#f1f5f9"},
                            {'range': [50, 80], 'color': "#e2e8f0"},
                            {'range': [80, 100], 'color': "#cbd5e1"}
                        ]
                    }
                ))
                fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'family': "Inter"})
                st.plotly_chart(fig, width='stretch')
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Candidate Name", parsed_data.get('name', 'N/A'))
                m2.metric("ATS Compatibility", f"{analysis_data.get('ats_compatibility', 0)}%")
                m3.metric("Experience", f"{len(parsed_data.get('experience', []))} roles")
                
                st.markdown("<hr style='border-color: #f1f5f9;'/>", unsafe_allow_html=True)
                
                # Feedback sections
                st.markdown("#### Strategic Insights")
                st.info(f"**General Assessment:**\n{analysis_data.get('feedback', {}).get('general', 'No general feedback provided.')}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.warning("**Areas for Development**")
                    for skill in analysis_data.get('missing_skills', []):
                        st.markdown(f"• <span style='color: #475569;'>{skill}</span>", unsafe_allow_html=True)
                with col_b:
                    st.success("**Optimization Opportunities**")
                    for sug in analysis_data.get('improvement_suggestions', []):
                        st.markdown(f"• <span style='color: #475569;'>{sug}</span>", unsafe_allow_html=True)

                if analysis_data.get('rewritten_bullets'):
                    st.markdown("<br/>", unsafe_allow_html=True)
                    st.markdown("#### Content Refinements")
                    for i, bullet in enumerate(analysis_data['rewritten_bullets']):
                        with st.expander(f"Refinement #{i+1}"):
                            st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; margin-bottom: 0.2rem;'>Original</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color: #334155;'>{bullet.get('original', '')}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; margin-bottom: 0.2rem; margin-top: 1rem;'>Proposed Revision</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color: #0f172a; font-weight: 500;'>{bullet.get('suggested', '')}</p>", unsafe_allow_html=True)
            else:
                st.info("Upload a document to view analytics.")

    with tabs[1]:
        st.markdown("### Processed Documents")
        try:
            history = resumes_collection.find({"user_email": "guest@example.com"})
            if history:
                df = pd.DataFrame([
                    {
                        "Candidate File": h.get('filename', 'Unknown'), 
                        "Score": h.get('analysis', {}).get('score', 0),
                        "Date Processed": h.get('created_at', 'Recent')
                    } for h in history
                ])
                # Clean dataframe styling
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.markdown("<p style='color: #64748b;'>No processing history available.</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load history: {str(e)}")

    with tabs[2]:
        st.markdown("### Interview Preparation Module")
        st.markdown("<p style='color: #64748b;'>Generate contextual behavioral and technical questions based on the active candidate profile.</p>", unsafe_allow_html=True)
        
        if 'analysis' in st.session_state:
            if st.button("Synthesize Question Bank"):
                with st.spinner("Generating targeted questions..."):
                    try:
                        questions = generate_questions(st.session_state.analysis.get("raw_text", ""))
                        st.session_state.questions = questions
                    except Exception as e:
                        st.error(f"Failed to generate questions: {str(e)}")
            
            if st.session_state.get('questions'):
                st.markdown("<br/>", unsafe_allow_html=True)
                for i, q in enumerate(st.session_state.questions):
                    st.markdown(f"""
                    <div style='background-color: #f8fafc; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 1rem;'>
                        <span style='color: #64748b; font-weight: 600; font-size: 0.8rem; text-transform: uppercase;'>Question {i+1}</span>
                        <p style='color: #0f172a; font-weight: 500; font-size: 1.1rem; margin-top: 0.5rem; margin-bottom: 0;'>{q}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Active analysis required to synthesize questions.")

if __name__ == "__main__":
    dashboard()
