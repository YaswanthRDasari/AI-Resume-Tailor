from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.tailoring import process_resume
from app.utils import extract_text_from_pdf

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
    resume_text = extract_text_from_pdf(resume_file.file)
    return process_resume(resume_text, job_description)
