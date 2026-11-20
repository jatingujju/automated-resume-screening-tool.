# 1. Project Explanation, Tech Stack and Architecture

## What is an Automated Resume Screening Tool?
Software that reads many resumes, compares each one with a job description, and produces a ranked list of the best matches.

### Simple explanation
Imagine 200 people apply for one job. A recruiter would need hours to read every resume. This tool does the first pass in seconds: it looks for the skills the job needs, checks experience, gives each candidate a score, and shows who to call first and why.

### Technical explanation
The pipeline extracts text from PDF/DOCX/TXT files, normalizes it, extracts structured features (skills, years of experience), computes TF-IDF cosine similarity between the job description and each resume, combines the features into a weighted score, applies rule gates (must-have skills, stuffing check) and exports a ranked report.

## What problem does it solve? Why does it matter?
- **Volume:** popular jobs get hundreds of applications.
- **Speed:** shortens time-to-shortlist, so good candidates are not lost.
- **Consistency:** every resume is judged by the same rules, reducing random human variation.
- **Focus:** recruiters spend time interviewing instead of reading.

## How ATS systems shortlist
Applicant Tracking Systems parse resumes into fields, then match **keywords/skills**, **experience**, **education** and **job-description similarity**. Many also apply hard filters ("must know SQL", "minimum 2 years"). This project copies that approach in a simple, explainable way.

## How this project compares resumes with job requirements
1. Job description (text) + required skills (config) define the target.
2. Each resume is converted to text and cleaned.
3. Skills and experience are extracted from the resume.
4. TF-IDF cosine similarity measures overall wording overlap with the JD.
5. Must-have / nice-to-have coverage and experience are measured.
6. A weighted score ranks everyone; rules decide shortlist / manual review / reject.

## Workflow
```
resume upload -> text extraction -> cleaning -> skill extraction
   -> job description matching -> score calculation
   -> shortlist / reject decision -> report generation
```

---

# 2. Tech Stack Options

| | Option A - Easy | Option B - Intermediate (**built here**) | Option C - Advanced |
|---|---|---|---|
| Libraries | Python, Pandas, Regex, plain keyword counting | + pdfplumber, python-docx, scikit-learn TF-IDF, cosine similarity, Matplotlib; optional Streamlit/FastAPI | + spaCy NER, sentence-transformers embeddings, SQLite/Postgres, FastAPI, Next.js, Docker |
| Difficulty | Beginner | Beginner-Intermediate | Advanced |
| Output | Keyword match % in a CSV | Ranked score, decisions, explanations, CSV, chart | Full web app with API, database, audit log, semantic ranking |

**Best for students: Option B.** It uses the libraries asked for in the project brief, runs on any laptop with no model downloads, is fully explainable in an interview, and leaves a clear upgrade path to Option C (the step-by-step section of your Word file describes Option C).

---

# 3. Project Architecture

```
            INPUT                         PROCESSING                           OUTPUT
 +------------------------+   +------------------------------------+   +-----------------------+
 | resumes/ (PDF,DOCX,TXT)|-->| extractor.py  : read raw text      |   | ranking_report.csv    |
 | data/job_description   |   | cleaner.py    : redact + normalize |   | shortlisted_*.csv     |
 | data/job_config.json   |-->| skills.py     : skills + years     |-->| rejected_*.csv        |
 |  (must-have skills,    |   | scorer.py     : TF-IDF + cosine,   |   | score_chart.png       |
 |   min years, threshold)|   |                 score, rank, rules |   | console table         |
 +------------------------+   +------------------------------------+   +-----------------------+
                                           |                                      ^
                                           +---------- report.py -----------------+
```

### Data flow
1. `main.py` loads the job (`load_job`) and all resumes (`load_resumes`).
2. For each resume: `normalize_text` -> `extract_skills` + `extract_years_experience`.
3. `tfidf_similarity` vectorizes the JD and all resumes together and returns one cosine value per resume.
4. `screen_resumes` computes coverage, score, stuffing flag, decision and reason text, and returns a DataFrame.
5. `report.py` writes CSVs, prints the table and draws the chart.
