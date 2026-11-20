"""
api/app.py - Optional FastAPI service (the 'serving' layer).

Run:   uvicorn api.app:app --reload
Docs:  http://127.0.0.1:8000/docs   (interactive Swagger page)

POST /screen  : send a job (form fields) + resume files, get ranked JSON back.
"""

from typing import List

from fastapi import FastAPI, File, Form, UploadFile

from src.extractor import bytes_to_file, extract_text
from src.scorer import JobConfig, screen_resumes

app = FastAPI(title="Automated Resume Screening API", version="1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/screen")
async def screen(
    title: str = Form("Data Analyst"),
    jd_text: str = Form(...),
    must_have: str = Form("sql,excel,python"),          # comma separated
    nice_to_have: str = Form(""),
    min_experience_years: float = Form(2.0),
    shortlist_threshold: float = Form(60.0),
    files: List[UploadFile] = File(...),
):
    resumes = []
    for f in files:
        data = await f.read()
        text = extract_text(bytes_to_file(data), filename=f.filename)
        if text.strip():
            resumes.append({"file_name": f.filename, "raw_text": text})

    job = JobConfig(
        title=title,
        description=jd_text,
        must_have=[s.strip().lower() for s in must_have.split(",") if s.strip()],
        nice_to_have=[s.strip().lower() for s in nice_to_have.split(",") if s.strip()],
        min_experience_years=min_experience_years,
        shortlist_threshold=shortlist_threshold,
    )
    df = screen_resumes(resumes, job)
    return {"job": title, "count": len(df), "results": df.to_dict(orient="records")}
