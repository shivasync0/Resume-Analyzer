import PyPDF2 # Pure Python PDF library (no extra software needed)
import docx # Pure Python Word library
import io

def parse_pdf(file_bytes):
    """
    Simplified PDF Parser: Uses pure Python to extract text.
    No Tesseract or Poppler required.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes)) 
        text = "" 
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def parse_docx(file_bytes):
    """
    Extracts text from a Word document using pure Python.
    """
    try:
        doc = docx.Document(io.BytesIO(file_bytes)) 
        text = "" 
        for para in doc.paragraphs:
            text += para.text + "\n" 
        return text 
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text(file_bytes, filename):
    """
    Main entry point for text extraction.
    """
    if filename.lower().endswith('.pdf'):
        return parse_pdf(file_bytes) 
    elif filename.lower().endswith('.docx'):
        return parse_docx(file_bytes) 
    else:
        # Fallback for plain text or other simple formats
        try:
            return file_bytes.decode('utf-8')
        except:
            raise ValueError("Unsupported format. Please upload PDF or DOCX.")
