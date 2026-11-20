# 10. GitHub Upload Steps

## Repository details (copy-paste)
- **Repo name:** `Automated-Resume-Screening-Tool`
- **Description:** `Python NLP tool that extracts skills from PDF/DOCX resumes, scores them against a job description with TF-IDF and cosine similarity, and generates ranked shortlist reports.`
- **Topics/tags:** `python` `nlp` `resume-screening` `resume-parser` `tf-idf` `cosine-similarity` `scikit-learn` `pandas` `hr-tech` `ats` `automation` `streamlit` `fastapi`
- **Visibility:** Public. **Do not** tick "Add README" or ".gitignore" on GitHub (you already have them).

## One-time setup
```bash
git --version                                   # install Git if this fails: https://git-scm.com
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

## Step by step
1. On github.com click **New repository**, enter the name and description above, choose **Public**, click **Create repository**.
2. In your terminal, go to the project folder:
   ```bash
   cd Automated-Resume-Screening-Tool
   git init
   git branch -M main
   ```
3. Commit in small steps (see messages below), for example:
   ```bash
   git add .gitignore requirements.txt
   git commit -m "Initial commit: project structure and requirements"
   ```
4. Connect and push (replace `YOUR-USERNAME`):
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/Automated-Resume-Screening-Tool.git
   git push -u origin main
   ```
   GitHub asks you to sign in. If a password is rejected, use a **Personal Access Token** (GitHub -> Settings -> Developer settings -> Tokens) or GitHub Desktop.
5. Add the repo topics: repository page -> gear icon next to **About** -> add topics + description.
6. Refresh the page and check that the README, images and CSVs display.

## Suggested commit sequence
| Commit | Files | Message |
|---|---|---|
| 1 | `.gitignore`, `requirements.txt` | `Initial commit: project structure and requirements` |
| 2 | `src/generate_samples.py`, `resumes/`, `data/` | `Add synthetic sample resumes and job description` |
| 3 | `src/extractor.py`, `src/cleaner.py` | `Add resume text extraction and cleaning` |
| 4 | `src/skills.py` | `Add skill and experience extraction` |
| 5 | `src/scorer.py` | `Add TF-IDF scoring, ranking and shortlist rules` |
| 6 | `src/report.py`, `main.py`, `tests/` | `Add report generation, CLI and tests` |
| 7 | `outputs/`, `images/` | `Add generated reports and screenshots` |
| 8 | `app_streamlit.py`, `api/` | `Add optional Streamlit dashboard and FastAPI service` |
| 9 | `README.md`, `docs/` | `Add README and documentation` |

Push after the last commit (or after each one): `git push`.

## Uploading screenshots and output files
Put screenshots in `images/` and CSVs in `outputs/`, then:
```bash
git add images outputs
git commit -m "Add screenshots and output reports"
git push
```
Link images in the README with `![caption](images/your_screenshot.png)`.

## Common mistakes
- Committing `venv/` (the `.gitignore` already prevents this)
- Uploading real people's resumes or personal data
- One giant commit with the message "final"
- Broken image links: file names are case-sensitive and must match exactly
