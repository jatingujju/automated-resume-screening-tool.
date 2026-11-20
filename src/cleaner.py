"""
cleaner.py
----------
Phase 6: Text cleaning.

Two levels of cleaning are used:
  * normalize_text()  - light cleaning, keeps symbols such as "c++" or "scikit-learn"
                        (used for skill matching and experience extraction)
  * clean_for_tfidf() - heavy cleaning for TF-IDF (lowercase, only letters/numbers)

Both remove e-mails, phone numbers and links first. This is also a
fairness/privacy step: contact details should never influence a score.
"""

import re

EMAIL_RE = re.compile(r"[\w\.\-+]+@[\w\-]+\.[\w\.\-]+")
URL_RE = re.compile(r"(https?://\S+|www\.\S+|linkedin\.com/\S+|github\.com/\S+)", re.I)
PHONE_RE = re.compile(r"(\+?\d[\d\s\-()]{8,}\d)")


def redact_contact_info(text: str) -> str:
    """Remove e-mails, links and phone numbers."""
    text = EMAIL_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = PHONE_RE.sub(" ", text)
    return text


def normalize_text(text: str) -> str:
    """Light cleaning: redact contact info, lowercase, squeeze whitespace."""
    text = redact_contact_info(text)
    text = text.lower()
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def clean_for_tfidf(text: str) -> str:
    """Heavy cleaning for TF-IDF: keep only letters/numbers/+/#."""
    text = normalize_text(text)
    text = re.sub(r"[^a-z0-9+#\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def guess_candidate_name(raw_text: str, fallback: str = "Unknown") -> str:
    """The first non-empty line of a resume is usually the candidate's name."""
    for line in raw_text.splitlines():
        line = line.strip()
        if line and "@" not in line and len(line.split()) <= 5:
            return line.title() if line.isupper() else line
    return fallback
