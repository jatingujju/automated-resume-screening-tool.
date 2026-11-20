"""Basic tests. Run with:  python -m pytest   (or)   python tests/test_pipeline.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cleaner import normalize_text, redact_contact_info
from src.extractor import load_resumes
from src.scorer import load_job, screen_resumes
from src.skills import extract_skills, extract_years_experience


def test_skill_matching_is_word_safe():
    found = extract_skills(normalize_text("Worked with MySQL, Power BI and scikit-learn."))
    assert "sql" in found          # via the mysql alias
    assert "power bi" in found
    assert "scikit-learn" in found
    assert "java" not in found     # must not match inside "javascript"-like words


def test_years_experience():
    assert extract_years_experience("5+ years of experience in analytics") == 5.0
    assert extract_years_experience("experience: 3 years") == 3.0
    assert extract_years_experience("b.tech 4 years, no work history") == 0.0


def test_contact_info_removed():
    text = redact_contact_info("mail me at a.b@example.com or +91 98765 43210")
    assert "@" not in text and "98765" not in text


def test_full_pipeline_on_samples():
    job = load_job("data/job_config.json", "data/job_description.txt")
    df = screen_resumes(load_resumes("resumes"), job)
    assert len(df) == 10
    assert df.iloc[0]["rank"] == 1 and df["score"].is_monotonic_decreasing
    # nobody missing a must-have may be shortlisted
    shortlisted = df[df.status == "SHORTLISTED"]
    assert (shortlisted["must_have_missing"] == "").all()
    # the keyword-stuffed resume is never auto-shortlisted
    stuffed = df[df.resume_file.str.contains("Keywords")].iloc[0]
    assert stuffed.status == "MANUAL REVIEW"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
