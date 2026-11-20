# 6. Installation Guide and 9. How to Run

## Python setup
1. Install Python 3.9 or newer from https://www.python.org/downloads/ (on Windows tick **Add Python to PATH**).
2. Check: `python --version` (Windows) or `python3 --version` (Mac).

## Virtual environment + libraries
**Windows (Command Prompt / PowerShell)**
```
cd Automated-Resume-Screening-Tool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
**Mac / Linux**
```
cd Automated-Resume-Screening-Tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
If PowerShell blocks activation: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Run the project
```
python main.py                      # full screening, writes outputs/ and images/
python main.py --threshold 70       # stricter shortlist
python tests/test_pipeline.py       # run tests (or: python -m pytest)
streamlit run app_streamlit.py      # optional dashboard
uvicorn api.app:app --reload        # optional API, docs at http://127.0.0.1:8000/docs
```

## Expected terminal output (real output from this project)
```
[1/4] Job loaded: Data Analyst
      Must-have : sql, excel, python
      Nice-to-have: power bi, tableau, pandas, statistics, data visualization, data cleaning
[2/4] Extracted text from 10 resumes in 'resumes/'
[3/4] Scored and ranked candidates

====================================================================================================
 AUTOMATED RESUME SCREENING REPORT  |  Job: Data Analyst
====================================================================================================
 rank candidate_name  score must_have_missing  years_experience        status
    1    Aarav Mehta   89.0                                 3.0   SHORTLISTED
    2    Divya Reddy   81.0                                 6.0   SHORTLISTED
    3   Ananya Desai   78.6                                 2.0   SHORTLISTED
    4  Siddharth Rao   65.8                                 0.0 MANUAL REVIEW
    5     Priya Nair   65.1            python               4.0      REJECTED
    6     Rohan Iyer   59.0             excel               5.0      REJECTED
    7 Sneha Kulkarni   50.5                                 0.0      REJECTED
    8   Vikram Singh   48.1             excel               4.0      REJECTED
    9    Karan Patel   35.4       sql, python               3.0      REJECTED
   10    Meera Joshi   34.6       sql, python               5.0      REJECTED
====================================================================================================
 Summary: REJECTED: 6 | SHORTLISTED: 3 | MANUAL REVIEW: 1
====================================================================================================

[4/4] Reports saved:
      ranking      -> outputs/ranking_report.csv
      shortlisted  -> outputs/shortlisted_candidates.csv
      rejected     -> outputs/rejected_candidates.csv
      chart        -> images/score_chart.png
```

## Generated files
- `outputs/ranking_report.csv` - all candidates, ranked, with reasons
- `outputs/shortlisted_candidates.csv` - only SHORTLISTED
- `outputs/rejected_candidates.csv` - REJECTED and MANUAL REVIEW
- `images/score_chart.png` - bar chart

## Sample shortlist result
| Rank | Candidate | Score | Reason |
|---|---|---|---|
| 1 | Aarav Mehta | 89.0 | Matched 3/3 must-have skills; 3 yrs experience (needs 2) |
| 2 | Divya Reddy | 81.0 | Matched 3/3 must-have skills; 6 yrs experience (needs 2) |
| 3 | Ananya Desai | 78.6 | Matched 3/3 must-have skills; 2 yrs experience (needs 2) |

## Troubleshooting
| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the venv, then `pip install -r requirements.txt` |
| "No text found ... scanned PDF" | The PDF is an image; use a text-based PDF (OCR is not included) |
| Run from the wrong folder | `cd` into the project root (where `main.py` is) |
