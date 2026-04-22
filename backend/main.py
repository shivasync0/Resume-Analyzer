from flask import Flask, request, jsonify # Importing Flask framework and web utilities
from flask_cors import CORS # Library to allow the frontend (Streamlit) to talk to the backend
import os # For environment and path management
from backend.database import users_collection, resumes_collection # Importing our DB containers
from backend.parser import extract_text # Resume parsing helper
from backend.ai_engine import analyze_resume, generate_questions # AI processing helpers
from bson import ObjectId # MongoDB utility to handle unique ID strings

# Initializing the Flask application
# Why: This 'app' object is the core of your server that handles all incoming traffic.
app = Flask(__name__)

# Enabling Cross-Origin Resource Sharing (CORS)
# Why: By default, browsers block apps from talking to different servers. This 'unlocks' it.
CORS(app)

@app.route("/", methods=["GET"])
def read_root():
    """
    Route: / (Root)
    Purpose: A simple 'Health Check' to see if the server is alive.
    """
    return jsonify({"message": "AI Resume Analyzer Flask API is running"})



@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Route: /analyze
    Purpose: The core feature. Uploads, parses, and analyzes a resume using AI.
    """
    try:
        current_user_email = "guest@example.com"
        # Getting the uploaded file from the request
        file = request.files.get("file")
        # Getting the job description from the form
        job_description = request.form.get("job_description", "")
        
        if not file:
            return jsonify({"message": "No file uploaded"}), 400
            
        # Reading the raw bytes of the file
        content = file.read()
        
        # Calling our parser to extract text (PDF or DOCX)
        raw_text = extract_text(content, file.filename)
        
        # Sending the text to Gemini AI for deep analysis
        analysis_result = analyze_resume(raw_text, job_description)
        
        # Preparing the final document to store in MongoDB
        resume_doc = {
            "user_email": current_user_email,
            "filename": file.filename,
            "raw_text": raw_text,
            "job_description": job_description,
            "parsed_data": analysis_result["parsedData"],
            "analysis": analysis_result["analysis"]
        }
        
        # Inserting the analysis into the database
        inserted = resumes_collection.insert_one(resume_doc)
        # Adding the database ID to our JSON response
        resume_doc["_id"] = str(inserted.inserted_id)
        
        return jsonify(resume_doc), 200
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route("/history", methods=["GET"])
def get_history():
    """
    Route: /history
    Purpose: Shows all past resume analyses.
    """
    current_user_email = "guest@example.com"
    # Finding all documents where user_email matches our default guest
    cursor = resumes_collection.find({"user_email": current_user_email})
    history = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)
    return jsonify(history), 200

@app.route("/questions/<resume_id>", methods=["GET"])
def questions(resume_id):
    """
    Route: /questions/<resume_id>
    Purpose: Generates interview questions for a specific past analysis.
    """
    # Finding the specific resume by its Unique ID
    resume = resumes_collection.find_one({"_id": ObjectId(resume_id)})
    
    if not resume:
        return jsonify({"message": "Resume not found"}), 404
    
    # Asking AI to generate 5 questions based on the stored text
    q_list = generate_questions(resume["raw_text"])
    return jsonify({"questions": q_list}), 200

# Entry point: This starts the server when you run 'python main.py'
if __name__ == "__main__":
    # Numerical Value: '8000' is the port. If you change it to '5000', the URL changes.
    # 'debug=True' allows the server to restart automatically when you change code.
    app.run(host="0.0.0.0", port=8000, debug=True)
