# 12. Proof Building Strategy (6 Days) and 13. Screenshots / Outputs

| Day | Goal | What to do | What to commit | Commit message | Screenshot to save |
|---|---|---|---|---|---|
| 1 | Setup | Create venv, install libraries, create folders, generate sample resumes | `.gitignore`, `requirements.txt`, `resumes/`, `data/`, `src/generate_samples.py` | `Initial commit: setup, sample resumes and job description` | Project folder tree; `resumes/` folder |
| 2 | Resume text extraction | Run extractor on PDF, DOCX, TXT; print a short preview of each | `src/extractor.py`, `src/cleaner.py` | `Add resume text extraction and cleaning` | Terminal showing extracted text of one resume |
| 3 | Job description matching | Run skill + experience extraction; show matched/missing skills | `src/skills.py` | `Add skill and experience extraction` | Terminal showing matched skills per resume |
| 4 | Scoring and ranking | Add TF-IDF scoring, weights, rules; run `main.py` | `src/scorer.py`, `main.py` | `Add TF-IDF scoring, ranking and shortlist rules` | Terminal ranking table |
| 5 | Report generation | Save CSVs and chart; run tests | `src/report.py`, `outputs/`, `images/`, `tests/` | `Add report generation, outputs and tests` | Shortlist CSV opened in Excel; score chart |
| 6 | GitHub documentation | README, docs, optional Streamlit/FastAPI; push everything | `README.md`, `docs/`, `app_streamlit.py`, `api/` | `Add README, docs and optional dashboard/API` | GitHub repo home page; README preview |

> Tip: do the work on the real days and commit on the real days. Your GitHub commit history is the proof, so it should be honest.

## Exactly what to capture (screenshot checklist)
- [ ] **Project folder** - file explorer or `tree` showing all folders
- [ ] **Sample resumes** - the `resumes/` folder (and one resume opened)
- [ ] **Terminal output** - after `python main.py` (the full report)
- [ ] **Resume score output** - the `score` and `reason` columns
- [ ] **Ranking table** - terminal table or `images/ranking_table.png`
- [ ] **Shortlisted candidates report** - `outputs/shortlisted_candidates.csv` opened in Excel
- [ ] **Generated CSV file** - `ranking_report.csv` opened in Excel
- [ ] **Score chart** - `images/score_chart.png`
- [ ] **Streamlit dashboard** (optional) - after uploading resumes
- [ ] **GitHub repo preview** - repository home page with README and topics

Take the screenshots from **your own run** on your computer, with your username/folder path visible - these are your proof.

## Sharing the proof (LinkedIn / Instagram)
**LinkedIn post idea**
> Built an **Automated Resume Screening Tool** in Python as part of my course project. It extracts text from PDF/DOCX resumes, matches skills with a job description using TF-IDF + cosine similarity, ranks candidates, flags missing must-have skills and exports shortlist reports. Tech: Python, Pandas, scikit-learn, pdfplumber, python-docx. Code on GitHub: <your repo link> #Python #NLP #HRTech #Automation #GitHub

**Instagram:** a carousel works well - slide 1 title, slide 2 workflow, slide 3 ranking chart, slide 4 terminal output, slide 5 GitHub link.
