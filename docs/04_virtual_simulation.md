# 8. Virtual Simulation of a Real HR Screening System

Because real company ATS data is not available, the project *simulates* a hiring round.

| Step in a real HR process | How this project simulates it |
|---|---|
| Candidates apply with resumes | `src/generate_samples.py` creates 10 fictional resumes in PDF, DOCX and TXT. Profiles are deliberately varied: 3 strong analysts, 1 with no Python, 1 with no Excel, a fresher, a backend developer, 2 unrelated roles (marketing, HR) and 1 keyword-stuffed resume |
| HR writes the job post | `data/job_description.txt` (Data Analyst) |
| HR lists required skills | `data/job_config.json`: must-have `sql, excel, python`; nice-to-have `power bi, tableau, pandas, statistics...`; min 2 years |
| ATS parses the resumes | `extractor.py` reads each file; `cleaner.py` removes contact details |
| ATS finds skills/experience | `skills.py` matches skills (with aliases) and reads "X years of experience" |
| ATS scores the match | `scorer.py`: TF-IDF cosine + must-have coverage + nice-to-have coverage + experience |
| ATS ranks candidates | DataFrame sorted by score (rank 1 = best) |
| Recruiter sees a shortlist | SHORTLISTED / MANUAL REVIEW / REJECTED + a written reason for each |

## Why the sample set is useful for proof
Each resume tests a different behaviour:
- **Aarav, Divya, Ananya** - good matches, should be shortlisted
- **Priya** (no Python) and **Rohan** (no Excel) - strong, but a must-have gap blocks shortlisting
- **Sneha** - fresher with 0 years experience stated
- **Vikram** - skilled developer, wrong role
- **Karan, Meera** - unrelated profiles, lowest scores
- **Siddharth** - repeats skill names; flagged for MANUAL REVIEW instead of ranking high silently

## Things to try (makes your project look original)
1. Change must-have skills to `sql, power bi` and re-run - the ranking changes.
2. Raise `--threshold` to 80 and see fewer shortlisted candidates.
3. Replace the job description with a "Python Developer" role and compare results.
4. Add your own synthetic resume to `resumes/`.

## Screenshots to capture / outputs to save / files to upload
See `06_proof_building_plan.md` for the exact list. In short: project folder, sample resumes, terminal output, ranking table, shortlisted CSV, chart, GitHub repo page. Upload `outputs/*.csv` and `images/*.png` to GitHub.
