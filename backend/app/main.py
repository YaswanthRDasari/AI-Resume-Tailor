from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from app.tailoring import process_resume
from app.utils import extract_text_from_pdf, extract_text_from_latex
import tempfile
import subprocess
import os

app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost:3000",
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
    job_description: str = Form(...)
):
    # SpooledTemporaryFile needs to be seeked to 0 before reading
    resume_file.file.seek(0)
    filename = resume_file.filename.lower()
    if filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_file.file)
    elif filename.endswith('.tex'):
        resume_text = extract_text_from_latex(resume_file.file)
    else:
        return {"error": "Unsupported file type. Please upload a PDF or LaTeX (.tex) file."}
    return process_resume(resume_text, job_description)

@app.post("/latex-to-pdf")
def latex_to_pdf(latex_code: str = Form(...)):
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")
        # Write LaTeX code to .tex file
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)
        # Run pdflatex to generate PDF
        try:
            subprocess.run([
                "pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return {"error": "Failed to compile LaTeX to PDF.", "details": e.stderr.decode("utf-8")}
        # Read PDF and return as response
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return Response(pdf_bytes, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=tailored_resume.pdf"
        })
