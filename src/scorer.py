"""
scorer.py
---------
Phases 8 & 9: Resume scoring, ranking and shortlist decision.

Final score (0-100) is a transparent weighted blend:

    score = 100 * ( W_TEXT * tfidf_similarity
                  + W_MUST * must_have_coverage
                  + W_NICE * nice_to_have_coverage
                  + W_EXP  * experience_score )

Decision rules (human-readable, easy to explain in an interview):
    SHORTLISTED   : score >= threshold AND must-have coverage >= min_must_coverage
                    AND no keyword-stuffing flag
    MANUAL REVIEW : keyword-stuffing suspected (a human should look)
    REJECTED      : everything else
"""

from dataclasses import dataclass, field
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .cleaner import clean_for_tfidf, guess_candidate_name, normalize_text
from .skills import extract_skills, extract_years_experience

# ---- tunable weights (must add up to 1.0) ----
WEIGHTS = {"text": 0.30, "must": 0.40, "nice": 0.10, "exp": 0.20}

# TF-IDF cosine values between a long JD and a resume are naturally small,
# so we divide by this "good match" level and cap at 1.0.
TFIDF_FULL_CREDIT = 0.35

# A skill mentioned this many times, or lots of skills with no experience, looks like stuffing.
STUFFING_REPEAT_LIMIT = 6
STUFFING_SKILL_COUNT = 9


@dataclass
class JobConfig:
    title: str
    description: str
    must_have: list = field(default_factory=list)
    nice_to_have: list = field(default_factory=list)
    min_experience_years: float = 2.0
    shortlist_threshold: float = 60.0      # minimum final score (0-100)
    min_must_coverage: float = 1.0         # 1.0 = ALL must-have skills required


def load_job(config_path: str, description_path: str) -> JobConfig:
    """Load job settings (JSON) and the job description text (TXT)."""
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    desc = Path(description_path).read_text(encoding="utf-8")
    return JobConfig(
        title=cfg["title"],
        description=desc,
        must_have=[s.lower() for s in cfg.get("must_have", [])],
        nice_to_have=[s.lower() for s in cfg.get("nice_to_have", [])],
        min_experience_years=float(cfg.get("min_experience_years", 2)),
        shortlist_threshold=float(cfg.get("shortlist_threshold", 60)),
        min_must_coverage=float(cfg.get("min_must_coverage", 1.0)),
    )


def tfidf_similarity(job_text: str, resume_texts: list) -> np.ndarray:
    """
    Cosine similarity between the job description and each resume
    using TF-IDF vectors (unigrams + bigrams).
    """
    corpus = [clean_for_tfidf(job_text)] + [clean_for_tfidf(t) for t in resume_texts]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    matrix = vectorizer.fit_transform(corpus)
    return cosine_similarity(matrix[0:1], matrix[1:]).flatten()


def _coverage(required: list, found: dict):
    """Return (matched_list, missing_list, coverage_fraction)."""
    matched = [s for s in required if s in found]
    missing = [s for s in required if s not in found]
    fraction = len(matched) / len(required) if required else 1.0
    return matched, missing, fraction


def _stuffing_flag(skills_found: dict, years: float) -> bool:
    repeated = any(count >= STUFFING_REPEAT_LIMIT for count in skills_found.values())
    many_no_exp = len(skills_found) >= STUFFING_SKILL_COUNT and years == 0
    return repeated or many_no_exp


def screen_resumes(resumes: list, job: JobConfig) -> pd.DataFrame:
    """
    Run the full screening pipeline.

    resumes : list of {"file_name": str, "raw_text": str}
    returns : DataFrame sorted by score (rank 1 = best)
    """
    if not resumes:
        return pd.DataFrame()

    similarities = tfidf_similarity(job.description, [r["raw_text"] for r in resumes])

    rows = []
    for resume, sim in zip(resumes, similarities):
        text = normalize_text(resume["raw_text"])
        skills_found = extract_skills(text)
        years = extract_years_experience(text)

        must_ok, must_missing, must_cov = _coverage(job.must_have, skills_found)
        nice_ok, _, nice_cov = _coverage(job.nice_to_have, skills_found)

        text_score = min(1.0, float(sim) / TFIDF_FULL_CREDIT)
        exp_score = min(1.0, years / job.min_experience_years) if job.min_experience_years else 1.0

        score = 100 * (
            WEIGHTS["text"] * text_score
            + WEIGHTS["must"] * must_cov
            + WEIGHTS["nice"] * nice_cov
            + WEIGHTS["exp"] * exp_score
        )

        stuffed = _stuffing_flag(skills_found, years)

        if stuffed:
            status = "MANUAL REVIEW"
        elif score >= job.shortlist_threshold and must_cov >= job.min_must_coverage:
            status = "SHORTLISTED"
        else:
            status = "REJECTED"

        # Plain-English explanation (explainability)
        reasons = [f"Matched {len(must_ok)}/{len(job.must_have)} must-have skills"]
        if must_missing:
            reasons.append("missing: " + ", ".join(must_missing))
        reasons.append(f"{years:g} yrs experience (needs {job.min_experience_years:g})")
        if stuffed:
            reasons.append("possible keyword stuffing - check manually")

        rows.append({
            "candidate_name": guess_candidate_name(resume["raw_text"]),
            "resume_file": resume["file_name"],
            "score": round(score, 1),
            "tfidf_similarity": round(float(sim), 3),
            "must_have_matched": ", ".join(must_ok),
            "must_have_missing": ", ".join(must_missing),
            "nice_to_have_matched": ", ".join(nice_ok),
            "years_experience": years,
            "status": status,
            "reason": "; ".join(reasons),
        })

    df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df
