"""
app_streamlit.py - Optional dashboard for the Resume Screening Tool.

Run:  streamlit run app_streamlit.py
"""

import streamlit as st

from src.extractor import bytes_to_file, extract_text
from src.scorer import JobConfig, screen_resumes

st.set_page_config(page_title="Automated Resume Screening Tool", layout="wide")
st.title("Automated Resume Screening Tool")
st.caption("Upload resumes, paste a job description, get a ranked shortlist with explanations.")

# ---------- Sidebar: job settings ----------
with st.sidebar:
    st.header("Job settings")
    title = st.text_input("Job title", "Data Analyst")
    must = st.text_input("Must-have skills (comma separated)", "sql, excel, python")
    nice = st.text_input("Nice-to-have skills", "power bi, tableau, pandas, statistics, data visualization")
    min_exp = st.number_input("Minimum years of experience", 0.0, 30.0, 2.0, 0.5)
    threshold = st.slider("Shortlist score threshold", 0, 100, 60)

jd_text = st.text_area(
    "Job description",
    "We need a Data Analyst with 2+ years of experience. Strong SQL, Excel and Python. "
    "Power BI or Tableau dashboards, statistics and data cleaning.",
    height=150,
)
files = st.file_uploader("Upload resumes (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"],
                         accept_multiple_files=True)

if st.button("Screen resumes", type="primary"):
    if not files:
        st.warning("Please upload at least one resume.")
    else:
        resumes = []
        for f in files:
            text = extract_text(bytes_to_file(f.read()), filename=f.name)
            if text.strip():
                resumes.append({"file_name": f.name, "raw_text": text})
            else:
                st.warning(f"No text found in {f.name} (scanned PDF?). Skipped.")

        job = JobConfig(
            title=title,
            description=jd_text,
            must_have=[s.strip().lower() for s in must.split(",") if s.strip()],
            nice_to_have=[s.strip().lower() for s in nice.split(",") if s.strip()],
            min_experience_years=min_exp,
            shortlist_threshold=float(threshold),
        )
        df = screen_resumes(resumes, job)
        if df.empty:
            st.error("No readable resumes.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Shortlisted", int((df.status == "SHORTLISTED").sum()))
            c2.metric("Manual review", int((df.status == "MANUAL REVIEW").sum()))
            c3.metric("Rejected", int((df.status == "REJECTED").sum()))
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("candidate_name")["score"])
            st.download_button("Download full report (CSV)", df.to_csv(index=False),
                               file_name="ranking_report.csv", mime="text/csv")
