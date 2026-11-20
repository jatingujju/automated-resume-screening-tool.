"""
skills.py
---------
Phase 7: Skill matching and experience extraction.

A small curated skills dictionary: canonical skill -> list of aliases.
You can extend it freely (add your own skills!).
"""

import re

SKILLS = {
    # --- core data skills ---
    "python": ["python", "python3"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sql server", "t-sql", "sqlite"],
    "excel": ["excel", "ms excel", "microsoft excel", "advanced excel", "vlookup", "pivot table", "pivot tables"],
    "power bi": ["power bi", "powerbi", "power-bi"],
    "tableau": ["tableau"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "statistics": ["statistics", "statistical analysis", "hypothesis testing", "a/b testing"],
    "data visualization": ["data visualization", "data visualisation", "dashboards", "dashboard"],
    "data cleaning": ["data cleaning", "data cleansing", "data wrangling"],
    "etl": ["etl", "data pipeline", "data pipelines"],
    "power query": ["power query"],
    "dax": ["dax"],
    "google analytics": ["google analytics"],
    "r": ["r programming", "rstudio"],
    # --- ML / AI ---
    "machine learning": ["machine learning", "ml models", "predictive modeling", "predictive modelling"],
    "deep learning": ["deep learning", "neural networks"],
    "nlp": ["nlp", "natural language processing"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    # --- engineering ---
    "java": ["java"],
    "javascript": ["javascript"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "html": ["html"],
    "css": ["css"],
    "spring": ["spring boot", "spring"],
    "git": ["git"],
    "github": ["github"],
    "docker": ["docker"],
    "linux": ["linux"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "mongodb": ["mongodb"],
    "rest api": ["rest api", "rest apis", "restful"],
}


def _compile_patterns():
    patterns = {}
    for skill, aliases in SKILLS.items():
        parts = [re.escape(a) for a in sorted(aliases, key=len, reverse=True)]
        # Not preceded/followed by a letter, digit, + or # (so "sql" will not match "mysql")
        patterns[skill] = re.compile(r"(?<![a-z0-9+#])(?:" + "|".join(parts) + r")(?![a-z0-9+#])")
    return patterns


_PATTERNS = _compile_patterns()


def extract_skills(normalized_text: str) -> dict:
    """
    Find skills in (already normalized, lowercase) text.
    Returns {skill: number_of_mentions}.
    """
    found = {}
    for skill, pattern in _PATTERNS.items():
        count = len(pattern.findall(normalized_text))
        if count:
            found[skill] = count
    return found


_YEARS_PATTERNS = [
    # "3 years of experience", "5+ years experience", "2 yrs of work experience"
    re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+[a-z]+){0,3}?\s+experience"),
    # "experience: 3 years", "experience of 4+ years"
    re.compile(r"experience\s*(?:of|:|-|–)?\s*(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)"),
]


def extract_years_experience(normalized_text: str) -> float:
    """
    Estimate years of experience from explicit statements such as
    "3 years of experience". Returns the largest number found (0.0 if none).
    Limitation: it does not read date ranges - see docs for improvement ideas.
    """
    best = 0.0
    for pattern in _YEARS_PATTERNS:
        for match in pattern.finditer(normalized_text):
            best = max(best, float(match.group(1)))
    return best
