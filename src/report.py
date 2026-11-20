"""
report.py
---------
Phase 10: Report generation (CSV files, console table, chart).
"""

from pathlib import Path

import pandas as pd


def save_reports(df: pd.DataFrame, out_dir: str) -> dict:
    """Write ranking_report.csv, shortlisted.csv and rejected.csv."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    paths = {
        "ranking": out / "ranking_report.csv",
        "shortlisted": out / "shortlisted_candidates.csv",
        "rejected": out / "rejected_candidates.csv",
    }
    df.to_csv(paths["ranking"], index=False)
    df[df["status"] == "SHORTLISTED"].to_csv(paths["shortlisted"], index=False)
    df[df["status"] != "SHORTLISTED"].to_csv(paths["rejected"], index=False)
    return {k: str(v) for k, v in paths.items()}


def print_table(df: pd.DataFrame, job_title: str) -> None:
    """Pretty console output (good for a terminal screenshot)."""
    cols = ["rank", "candidate_name", "score", "must_have_missing", "years_experience", "status"]
    line = "=" * 100
    print(line)
    print(f" AUTOMATED RESUME SCREENING REPORT  |  Job: {job_title}")
    print(line)
    print(df[cols].to_string(index=False))
    print(line)
    counts = df["status"].value_counts()
    print(" Summary: " + " | ".join(f"{k}: {v}" for k, v in counts.items()))
    print(line)


def save_chart(df: pd.DataFrame, path: str, job_title: str) -> None:
    """Horizontal bar chart of scores, coloured by decision."""
    import matplotlib

    matplotlib.use("Agg")  # no window needed
    import matplotlib.pyplot as plt

    colors = {"SHORTLISTED": "#2e7d32", "MANUAL REVIEW": "#f9a825", "REJECTED": "#c62828"}
    data = df.iloc[::-1]  # best candidate on top
    fig, ax = plt.subplots(figsize=(9, 0.55 * len(data) + 1.6))
    ax.barh(data["candidate_name"], data["score"], color=[colors[s] for s in data["status"]])
    for y, v in enumerate(data["score"]):
        ax.text(v + 0.8, y, f"{v:.1f}", va="center", fontsize=9)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Match score (0-100)")
    ax.set_title(f"Resume ranking - {job_title}")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors.values()]
    ax.legend(handles, colors.keys(), loc="lower right")
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
