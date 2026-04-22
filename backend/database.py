import sqlite3
import json
import os

DB_PATH = "resumes.db"

def init_db():
    """Initializes the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create resumes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            filename TEXT,
            raw_text TEXT,
            job_description TEXT,
            parsed_data TEXT,
            analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Mock objects to maintain compatibility with main.py without refactoring everything
class MockCollection:
    def insert_one(self, document):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resumes (user_email, filename, raw_text, job_description, parsed_data, analysis)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            document.get('user_email'),
            document.get('filename'),
            document.get('raw_text'),
            document.get('job_description'),
            json.dumps(document.get('parsed_data')),
            json.dumps(document.get('analysis'))
        ))
        inserted_id = cursor.lastrowid
        conn.commit()
        conn.close()
        class Result: pass
        r = Result()
        r.inserted_id = inserted_id
        return r

    def find(self, query):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Simplistic mapping of MongoDB find to SQL
        email = query.get("user_email", "guest@example.com")
        cursor.execute('SELECT * FROM resumes WHERE user_email = ? ORDER BY created_at DESC', (email,))
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "_id": str(row[0]),
                "user_email": row[1],
                "filename": row[2],
                "raw_text": row[3],
                "job_description": row[4],
                "parsed_data": json.loads(row[5]),
                "analysis": json.loads(row[6])
            })
        return results

    def find_one(self, query):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Handle lookup by ID
        if "_id" in query:
            from bson import ObjectId
            try:
                res_id = int(str(query["_id"]))
            except:
                res_id = 0
            cursor.execute('SELECT * FROM resumes WHERE id = ?', (res_id,))
        else:
            # Fallback for other queries
            cursor.execute('SELECT * FROM resumes LIMIT 1')
            
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "_id": str(row[0]),
                "user_email": row[1],
                "filename": row[2],
                "raw_text": row[3],
                "job_description": row[4],
                "parsed_data": json.loads(row[5]),
                "analysis": json.loads(row[6])
            }
        return None

# Initialize the DB file on import
init_db()

# These variables are what main.py imports
users_collection = MockCollection() # Not really used now since auth is gone
resumes_collection = MockCollection()
