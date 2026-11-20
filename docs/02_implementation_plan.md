# 4. Implementation Plan (11 Phases)

| # | Phase | What to do | Why | Expected output | Common beginner mistake |
|---|---|---|---|---|---|
| 1 | Setup | Install Python 3.9+, create a virtual environment, `pip install -r requirements.txt` | Isolated, reproducible environment | `pip list` shows pandas, scikit-learn... | Installing into the global Python; forgetting to activate the venv |
| 2 | Folder creation | Create `resumes/ data/ src/ outputs/ images/ docs/` | Clean, GitHub-ready structure | Folder tree matches README | Putting everything in one file/folder |
| 3 | Sample resumes | Run `python -m src.generate_samples` (10 synthetic resumes, mixed formats and quality) | No real ATS data available; also privacy-safe | 10 files in `resumes/` | Using real people's resumes (privacy risk) |
| 4 | Job description | Edit `data/job_description.txt` and `data/job_config.json` (must-have, nice-to-have, min years) | The "target" every resume is compared to | Two data files | Listing too many must-haves, so nobody qualifies |
| 5 | Text extraction | `src/extractor.py` reads PDF/DOCX/TXT | Parsing quality drives all later accuracy | Raw text per resume | Scanned PDFs return empty text (need OCR); not handling errors |
| 6 | Text cleaning | `src/cleaner.py` removes e-mail/phone/links, lowercases, trims spaces | Clean text = fair, accurate matching | Normalized text | Over-cleaning: deleting `+` and `#` turns `c++` into `c` |
| 7 | Skill matching | `src/skills.py` dictionary + regex word boundaries; years of experience | Turns free text into structured features | `{python: 3, sql: 2}` and `3.0` years | Matching `sql` inside `mysql`/`nosql` by accident; no aliases |
| 8 | Resume scoring | `src/scorer.py` TF-IDF cosine + coverage + experience -> weighted 0-100 score | One explainable number per candidate | Score column | Trusting raw cosine alone; weights that do not add to 1 |
| 9 | Ranking & shortlisting | Sort by score, apply rules (all must-haves, threshold, stuffing flag) | Gives actionable decisions | Rank + status columns | Shortlisting purely by score and ignoring missing must-haves |
| 10 | Report generation | `src/report.py` writes CSVs, table and chart | Recruiters need shareable output | 3 CSV files + chart in `outputs/` and `images/` | Forgetting `index=False`; overwriting reports without noticing |
| 11 | GitHub upload | `git init`, commit in small steps, push; add README + screenshots | Public proof of work | Live repository | One giant commit; committing `venv/` or real data |
