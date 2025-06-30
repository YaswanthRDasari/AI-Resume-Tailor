
from fastapi import FastAPI
from pydantic import BaseModel
from app.tailoring import process_resume

app = FastAPI()

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/tailor")
def tailor_resume(req: ResumeRequest):
    return process_resume(req.resume_text, req.job_description)
