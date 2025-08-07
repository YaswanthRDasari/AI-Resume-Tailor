from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from app.tailoring import process_resume
from app.utils import extract_text_from_pdf, extract_text_from_latex
import tempfile
import subprocess
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Resume Tailor API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is working correctly"}

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tailor")
def tailor_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    target_match_percentage: int = Form(0)
):
    try:
        # SpooledTemporaryFile needs to be seeked to 0 before reading
        resume_file.file.seek(0)
        filename = resume_file.filename.lower()
        
        print(f"[DEBUG] Processing file: {filename}")
        print(f"[DEBUG] Job description length: {len(job_description)}")
        
        if filename.endswith('.pdf'):
            try:
                resume_text = extract_text_from_pdf(resume_file.file)
                if not resume_text or len(resume_text.strip()) < 50:
                    return {"error": "The PDF file appears to be empty or contains no readable text. Please ensure the PDF contains text (not just images) and try again."}
            except Exception as pdf_error:
                print(f"[ERROR] PDF extraction failed: {str(pdf_error)}")
                if "Stream has ended unexpectedly" in str(pdf_error) or "PdfStreamError" in str(pdf_error):
                    return {"error": "The PDF file appears to be corrupted or invalid. Please upload a valid PDF file or try converting your document to PDF again."}
                else:
                    return {"error": f"Failed to extract text from PDF: {str(pdf_error)}"}
        elif filename.endswith('.tex'):
            try:
                resume_text = extract_text_from_latex(resume_file.file)
                if not resume_text or len(resume_text.strip()) < 50:
                    return {"error": "The LaTeX file appears to be empty or contains no readable content. Please check your file and try again."}
            except Exception as tex_error:
                print(f"[ERROR] LaTeX extraction failed: {str(tex_error)}")
                return {"error": f"Failed to extract text from LaTeX file: {str(tex_error)}"}
        else:
            return {"error": "Unsupported file type. Please upload a PDF or LaTeX (.tex) file."}
        
        print(f"[DEBUG] Extracted resume text length: {len(resume_text)}")
        
        result = process_resume(resume_text, job_description, target_match_percentage)
        print(f"[DEBUG] Process result keys: {list(result.keys()) if result else 'None'}")
        
        return result
    except Exception as e:
        print(f"[ERROR] Exception in tailor_resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error: {str(e)}"}

@app.post("/latex-to-pdf")
def latex_to_pdf(latex_code: str = Form(...)):
    """
    Convert LaTeX code to PDF with comprehensive error handling and fallback options
    """
    try:
        print(f"[DEBUG] Starting LaTeX to PDF conversion")
        print(f"[DEBUG] LaTeX code length: {len(latex_code)}")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, "resume.tex")
            pdf_path = os.path.join(tmpdir, "resume.pdf")
            log_path = os.path.join(tmpdir, "resume.log")
            
            # Write LaTeX code to .tex file
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(latex_code)
            
            print(f"[DEBUG] LaTeX file written to: {tex_path}")
            
            # Check if pdflatex is available
            try:
                subprocess.run(["pdflatex", "--version"], 
                             capture_output=True, check=True, timeout=10)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                return {"error": "pdflatex is not installed or not accessible. Please install LaTeX distribution (e.g., MiKTeX, TeX Live)."}
            
            # Run pdflatex to generate PDF with better error handling
            try:
                result = subprocess.run([
                    "pdflatex", 
                    "-interaction=nonstopmode", 
                    "-output-directory", tmpdir, 
                    tex_path
                ], capture_output=True, text=True, timeout=60)
                
                print(f"[DEBUG] pdflatex return code: {result.returncode}")
                print(f"[DEBUG] pdflatex stdout: {result.stdout[:500]}...")
                print(f"[DEBUG] pdflatex stderr: {result.stderr[:500]}...")
                
                # Check if PDF was actually created
                if not os.path.exists(pdf_path):
                    # Read log file for more details
                    log_content = ""
                    if os.path.exists(log_path):
                        with open(log_path, "r", encoding="utf-8") as f:
                            log_content = f.read()
                    
                    error_msg = "PDF file was not generated. "
                    if "! LaTeX Error" in log_content:
                        error_msg += "LaTeX compilation error detected."
                    elif result.stderr:
                        error_msg += f"Compilation error: {result.stderr[:200]}"
                    else:
                        error_msg += "Unknown compilation error."
                    
                    return {"error": error_msg, "details": log_content[:1000]}
                
                # Verify PDF file is not empty and is valid
                pdf_size = os.path.getsize(pdf_path)
                if pdf_size == 0:
                    return {"error": "Generated PDF file is empty."}
                
                print(f"[DEBUG] PDF file size: {pdf_size} bytes")
                
                # Read PDF and verify it starts with PDF header
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                
                if not pdf_bytes.startswith(b'%PDF'):
                    return {"error": "Generated file is not a valid PDF."}
                
                print(f"[DEBUG] PDF validation successful, returning {len(pdf_bytes)} bytes")
                
                return Response(
                    pdf_bytes, 
                    media_type="application/pdf", 
                    headers={
                        "Content-Disposition": "attachment; filename=tailored_resume.pdf",
                        "Content-Length": str(len(pdf_bytes))
                    }
                )
                
            except subprocess.TimeoutExpired:
                return {"error": "PDF generation timed out. The LaTeX code might be too complex."}
            except Exception as e:
                return {"error": f"PDF generation failed: {str(e)}"}
                
    except Exception as e:
        print(f"[ERROR] Exception in latex_to_pdf: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error during PDF generation: {str(e)}"}

@app.post("/latex-to-text")
def latex_to_text(latex_code: str = Form(...)):
    """
    Convert LaTeX code to plain text as a fallback when PDF generation fails
    """
    try:
        print(f"[DEBUG] Converting LaTeX to plain text")
        
        # Simple LaTeX to text conversion
        import re
        
        # Remove LaTeX commands and environments
        text = latex_code
        
        # Remove LaTeX comments
        text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
        
        # Remove LaTeX commands (basic)
        text = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{[^\}]*\})?', '', text)
        
        # Remove curly braces
        text = re.sub(r'[{}]', '', text)
        
        # Remove special LaTeX characters
        text = re.sub(r'\\[^\w]', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Add some formatting
        formatted_text = f"""
TAILORED RESUME (Plain Text Version)
{'=' * 50}

{text}

{'=' * 50}
Generated by AI Resume Tailor
        """.strip()
        
        return {
            "text_content": formatted_text,
            "message": "PDF generation failed, but here's a plain text version of your tailored resume."
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in latex_to_text: {str(e)}")
        return {"error": f"Failed to convert LaTeX to text: {str(e)}"}