"""
main.py - Automated Resume Screening Tool (command-line entry point)

Usage:
    python main.py
    python main.py --resumes resumes --threshold 65
"""

import argparse

from src.extractor import load_resumes
from src.report import print_table, save_chart, save_reports
from src.scorer import load_job, screen_resumes


def main():
    parser = argparse.ArgumentParser(description="Automated Resume Screening Tool")
    parser.add_argument("--resumes", default="resumes", help="folder with PDF/DOCX/TXT resumes")
    parser.add_argument("--job-config", default="data/job_config.json", help="job settings (JSON)")
    parser.add_argument("--job-desc", default="data/job_description.txt", help="job description (TXT)")
    parser.add_argument("--out", default="outputs", help="folder for CSV reports")
    parser.add_argument("--threshold", type=float, default=None, help="override shortlist score threshold")
    parser.add_argument("--no-chart", action="store_true", help="skip saving the score chart")
    args = parser.parse_args()

    # 1. Load job
    job = load_job(args.job_config, args.job_desc)
    if args.threshold is not None:
        job.shortlist_threshold = args.threshold
    print(f"[1/4] Job loaded: {job.title}")
    print(f"      Must-have : {', '.join(job.must_have)}")
    print(f"      Nice-to-have: {', '.join(job.nice_to_have)}")

    # 2. Extract resumes
    resumes = load_resumes(args.resumes)
    print(f"[2/4] Extracted text from {len(resumes)} resumes in '{args.resumes}/'")
    if not resumes:
        print("No readable resumes found. Add PDF/DOCX/TXT files and try again.")
        return

    # 3. Score + rank
    df = screen_resumes(resumes, job)
    print("[3/4] Scored and ranked candidates\n")
    print_table(df, job.title)

    # 4. Reports
    paths = save_reports(df, args.out)
    if not args.no_chart:
        save_chart(df, "images/score_chart.png", job.title)
    print("\n[4/4] Reports saved:")
    for name, path in paths.items():
        print(f"      {name:<12} -> {path}")
    if not args.no_chart:
        print("      chart        -> images/score_chart.png")


if __name__ == "__main__":
    main()
