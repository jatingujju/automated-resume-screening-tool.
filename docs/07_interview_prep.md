# 14. Interview Preparation

Each answer has a short **HR version** (non-technical) and a **Technical version**. Read the code once so you can explain it in your own words.

### 1. Explain your project.
**HR version:** I built a tool that reads resumes automatically and checks how well each one matches a job. It ranks candidates, shows which required skills are missing, and creates a shortlist report, so recruiters save time.
**Technical version:** It is a Python pipeline: extract text from PDF/DOCX/TXT with pdfplumber and python-docx, clean it with regex (removing contact details), extract skills and years of experience using a skills dictionary, compute TF-IDF cosine similarity with the job description, and combine similarity, must-have coverage, nice-to-have coverage and experience into a 0-100 score. Rules then decide SHORTLISTED, MANUAL REVIEW or REJECTED, and Pandas exports CSV reports.

### 2. What problem does it solve?
**HR:** Reading hundreds of resumes by hand is slow and inconsistent; this does the first filter quickly and the same way for everyone.
**Technical:** It automates first-round screening by turning unstructured resumes into structured features and ranking them against explicit job criteria.

### 3. Which technologies did you use and why?
Python for the whole pipeline; pdfplumber/pypdf and python-docx for file parsing; regex for cleaning and extraction; scikit-learn for TF-IDF and cosine similarity; Pandas for reports; Matplotlib for charts; optionally Streamlit and FastAPI. I chose them because they are standard, free and easy to explain.

### 4. How does the screening work step by step?
Load job -> extract text -> clean -> find skills/years -> TF-IDF similarity -> weighted score -> apply rules -> rank -> save reports.

### 5. What is TF-IDF and why use it?
TF-IDF gives each word a weight: high if it appears often in a document (TF) but low if it appears in almost every document (IDF). Common words matter less, distinctive words (like "tableau") matter more. It turns text into vectors so documents can be compared numerically.

### 6. What is cosine similarity?
It measures the angle between two vectors. Same direction (similar word usage) gives a value near 1; unrelated text gives near 0. It ignores document length, which suits resumes of different sizes.

### 7. How is the final score calculated? Why those weights?
`score = 100 x (0.30 text similarity + 0.40 must-have coverage + 0.10 nice-to-have coverage + 0.20 experience)`. Must-have skills carry the most weight because they are the real job requirements; text similarity supports it but can be fooled by wording. Weights are editable and I would tune them with labelled data.

### 8. What challenges did you face? (use real ones)
- Different file formats and scanned PDFs with no text layer
- `sql` wrongly matching inside other words - solved with word-boundary regex and aliases
- Keyword stuffing - solved with a repeat/no-experience check that sends the resume to manual review
- 0.67 vs 2/3 rounding bug in the must-have threshold - made the rule explicit (all must-haves required)

### 9. What are the limitations and how would you improve it?
Limitations: fixed skills dictionary, TF-IDF has no semantic understanding, experience read only from explicit statements, no OCR. Improvements: sentence-transformer embeddings, spaCy NER, date-range parsing, OCR, a database, a recruiter dashboard, and evaluation with labelled data (ROC-AUC, top-k precision).

### 10. How do you handle fairness and bias?
I remove e-mail, phone and links before scoring, never use name, gender, age, religion or location as features, give every decision a written reason, and send suspicious or borderline cases to manual review. The tool supports human decisions; it does not replace them. In real use I would also need candidate consent and regular bias audits.

---
## Bonus: 30-second pitch
"I built an automated resume screening tool in Python. It reads resumes in PDF, DOCX and text, extracts skills and experience, compares them with a job description using TF-IDF and cosine similarity, and produces a ranked shortlist with reasons, flagging missing must-have skills. The code and reports are on my GitHub."
