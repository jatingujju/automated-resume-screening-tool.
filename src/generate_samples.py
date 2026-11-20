"""
generate_samples.py
-------------------
Phase 3: Creates 10 SYNTHETIC resumes (fictional people, fake contact details)
in PDF, DOCX and TXT format, so the project can run without real candidate data.

Run:  python -m src.generate_samples
Needs: reportlab (only for generating sample PDFs), python-docx
"""

from pathlib import Path

OUT_DIR = Path("resumes")

# Each resume: name, title, contact, summary, skills, experience bullets, education, format
RESUMES = [
    {
        "file": "Aarav_Mehta_DataAnalyst", "fmt": "pdf",
        "name": "Aarav Mehta", "title": "Data Analyst",
        "contact": "aarav.mehta@example.com | +91 90000 11111 | Pune, India",
        "summary": "Data Analyst with 3 years of experience turning business data into dashboards and insights.",
        "skills": "SQL, Excel, Python, Pandas, Power BI, Tableau, Statistics, Data Visualization, Data Cleaning",
        "experience": [
            "Data Analyst, RetailKart (2022 - Present): wrote SQL queries on sales data, built Power BI dashboards for the regional team.",
            "Automated weekly Excel reports using Python and Pandas, saving 6 hours per week.",
            "Cleaned and analysed customer data, applied statistics to find churn drivers.",
        ],
        "education": "B.Sc. Statistics, Savitribai Phule Pune University",
    },
    {
        "file": "Priya_Nair_BusinessAnalyst", "fmt": "docx",
        "name": "Priya Nair", "title": "Business Analyst",
        "contact": "priya.nair@example.com | +91 90000 22222 | Mumbai, India",
        "summary": "Business Analyst with 4 years of experience in reporting and BI for the banking sector.",
        "skills": "SQL, Excel, Power BI, DAX, Power Query, Dashboards, Data Visualization",
        "experience": [
            "Business Analyst, FinServe Bank (2020 - Present): built Power BI dashboards and DAX measures for loan reporting.",
            "Wrote complex SQL Server queries and advanced Excel pivot tables for monthly MIS.",
            "Worked with stakeholders to gather reporting requirements.",
        ],
        "education": "MBA (Finance), Mumbai University",
    },
    {
        "file": "Rohan_Iyer_DataScientist", "fmt": "pdf",
        "name": "Rohan Iyer", "title": "Data Scientist",
        "contact": "rohan.iyer@example.com | +91 90000 33333 | Bengaluru, India",
        "summary": "Data Scientist with 5 years of experience building machine learning models and data pipelines.",
        "skills": "Python, SQL, Pandas, NumPy, Scikit-learn, Machine Learning, Matplotlib, Statistics, Git",
        "experience": [
            "Data Scientist, QuantAI (2019 - Present): built predictive modeling pipelines in Python and Scikit-learn.",
            "Used SQL and Pandas for data cleaning and feature engineering on large datasets.",
            "Presented model results using Matplotlib and data visualization.",
        ],
        "education": "M.Tech Data Science, IIT Madras",
    },
    {
        "file": "Sneha_Kulkarni_Fresher", "fmt": "txt",
        "name": "Sneha Kulkarni", "title": "Fresher - Aspiring Data Analyst",
        "contact": "sneha.kulkarni@example.com | +91 90000 44444 | Aurangabad, India",
        "summary": "Recent graduate with a 6 month internship, keen to start a career in data analysis.",
        "skills": "Python, SQL, Excel, Pandas, Data Visualization",
        "experience": [
            "Data Analyst Intern, LocalMart (6 months): cleaned sales data in Excel and Pandas.",
            "College project: sales dashboard using Python, Matplotlib and SQL.",
        ],
        "education": "B.E. Computer Science, Dr. Babasaheb Ambedkar Marathwada University",
    },
    {
        "file": "Vikram_Singh_BackendDeveloper", "fmt": "pdf",
        "name": "Vikram Singh", "title": "Backend Developer",
        "contact": "vikram.singh@example.com | +91 90000 55555 | Hyderabad, India",
        "summary": "Backend developer with 4 years of experience building REST APIs.",
        "skills": "Java, Spring Boot, Python, Django, MySQL, Docker, Git, REST APIs, AWS",
        "experience": [
            "Backend Developer, CloudNest (2020 - Present): built REST APIs with Spring Boot and Django.",
            "Designed MySQL schemas, deployed services using Docker on AWS.",
        ],
        "education": "B.Tech Information Technology, JNTU Hyderabad",
    },
    {
        "file": "Ananya_Desai_DataAnalyst", "fmt": "docx",
        "name": "Ananya Desai", "title": "Data Analyst",
        "contact": "ananya.desai@example.com | +91 90000 66666 | Nagpur, India",
        "summary": "Data Analyst with 2 years of experience in e-commerce analytics.",
        "skills": "SQL, Excel, Python, Power BI, Google Analytics, Data Visualization",
        "experience": [
            "Data Analyst, ShopEasy (2023 - Present): analysed funnel and campaign data with SQL and Google Analytics.",
            "Built Power BI dashboards and Excel reports for the marketing team.",
            "Used Python for data cleaning and basic statistics.",
        ],
        "education": "B.Com (Computer Applications), Nagpur University",
    },
    {
        "file": "Karan_Patel_MarketingExecutive", "fmt": "pdf",
        "name": "Karan Patel", "title": "Digital Marketing Executive",
        "contact": "karan.patel@example.com | +91 90000 77777 | Ahmedabad, India",
        "summary": "Marketing executive with 3 years of experience in SEO and campaign reporting.",
        "skills": "Excel, Google Analytics, SEO, Social Media Marketing, Content Writing",
        "experience": [
            "Digital Marketing Executive, BrandBox (2021 - Present): ran SEO and paid campaigns.",
            "Prepared campaign reports in Excel and Google Analytics.",
        ],
        "education": "BBA Marketing, Gujarat University",
    },
    {
        "file": "Meera_Joshi_HRExecutive", "fmt": "docx",
        "name": "Meera Joshi", "title": "HR Executive",
        "contact": "meera.joshi@example.com | +91 90000 88888 | Nashik, India",
        "summary": "HR Executive with 5 years of experience in recruitment, payroll and employee engagement.",
        "skills": "Recruitment, Payroll, Onboarding, Employee Engagement, MS Excel",
        "experience": [
            "HR Executive, PeopleFirst (2019 - Present): handled end-to-end recruitment and payroll.",
            "Maintained employee records in MS Excel.",
        ],
        "education": "MBA (HR), Pune University",
    },
    {
        "file": "Siddharth_Rao_Keywords", "fmt": "pdf",
        "name": "Siddharth Rao", "title": "Data Analyst",
        "contact": "siddharth.rao@example.com | +91 90000 99999 | Chennai, India",
        "summary": "Python Python SQL SQL Excel Excel Power BI Power BI Tableau Pandas Python SQL Excel.",
        "skills": ("Python, Python, Python, SQL, SQL, SQL, Excel, Excel, Excel, Power BI, Power BI, Tableau, "
                   "Pandas, Statistics, Data Cleaning, Data Visualization, Python, SQL, Excel, Python, SQL, Excel"),
        "experience": [
            "Python SQL Excel Power BI Tableau Pandas Statistics.",
        ],
        "education": "B.Sc. Mathematics",
    },
    {
        "file": "Divya_Reddy_SeniorDataAnalyst", "fmt": "txt",
        "name": "Divya Reddy", "title": "Senior Data Analyst",
        "contact": "divya.reddy@example.com | +91 91111 00000 | Hyderabad, India",
        "summary": "Senior Data Analyst with 6 years of experience leading analytics for supply chain and finance teams.",
        "skills": "SQL, Excel, Python, Pandas, Tableau, Power BI, ETL, Statistics, A/B Testing, Data Visualization, Data Cleaning",
        "experience": [
            "Senior Data Analyst, LogiTrack (2020 - Present): led a team of 3 analysts, built Tableau and Power BI dashboards.",
            "Designed ETL pipelines using SQL and Python, improved report refresh time by 40 percent.",
            "Ran A/B tests and statistical analysis to support pricing decisions.",
        ],
        "education": "M.Sc. Statistics, University of Hyderabad",
    },
]


def _lines(r):
    """Resume as a list of (kind, text) so every format can render it."""
    out = [("name", r["name"]), ("title", r["title"]), ("small", r["contact"]),
           ("head", "SUMMARY"), ("text", r["summary"]),
           ("head", "SKILLS"), ("text", r["skills"]),
           ("head", "EXPERIENCE")]
    out += [("bullet", b) for b in r["experience"]]
    out += [("head", "EDUCATION"), ("text", r["education"])]
    return out


def write_txt(r, path):
    lines = []
    for kind, text in _lines(r):
        if kind == "head":
            lines.append("")
        lines.append(("- " + text) if kind == "bullet" else text)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_docx(r, path):
    from docx import Document

    doc = Document()
    for kind, text in _lines(r):
        if kind == "name":
            doc.add_heading(text, level=0)
        elif kind == "head":
            doc.add_heading(text.title(), level=2)
        elif kind == "bullet":
            doc.add_paragraph(text, style="List Bullet")
        else:
            doc.add_paragraph(text)
    doc.save(path)


def write_pdf(r, path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    from xml.sax.saxutils import escape

    styles = getSampleStyleSheet()
    story = []
    for kind, text in _lines(r):
        text = escape(text)
        if kind == "name":
            story.append(Paragraph(text, styles["Title"]))
        elif kind == "head":
            story += [Spacer(1, 8), Paragraph(f"<b>{text}</b>", styles["Heading3"])]
        elif kind == "bullet":
            story.append(Paragraph("- " + text, styles["BodyText"]))
        else:
            story.append(Paragraph(text, styles["BodyText"]))
    SimpleDocTemplate(str(path), pagesize=A4).build(story)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    writers = {"pdf": write_pdf, "docx": write_docx, "txt": write_txt}
    for r in RESUMES:
        path = OUT_DIR / f"{r['file']}.{r['fmt']}"
        writers[r["fmt"]](r, path)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
