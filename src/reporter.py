"""
reporter.py
Generates ranking table, shortlist decisions, and saves CSV report.
"""
import os
import pandas as pd

SHORTLIST_THRESHOLD = 50.0  # Candidates scoring >= 50% are shortlisted

def build_report(names, filenames, tfidf_scores, skill_scores,
                 final_scores, required_skills, resume_texts) -> pd.DataFrame:
    required_lower = [s.lower().strip() for s in required_skills]
    matched_skills_list, missing_skills_list = [], []
    for text in resume_texts:
        text_lower = text.lower()
        matched = [s for s in required_lower if s in text_lower]
        missing = [s for s in required_lower if s not in text_lower]
        matched_skills_list.append(", ".join(matched))
        missing_skills_list.append(", ".join(missing) if missing else "None")

    df = pd.DataFrame({
        "Name":            names,
        "File":            filenames,
        "TF-IDF Score":    [f"{s*100:.1f}%" for s in tfidf_scores],
        "Skill Match":     [f"{s*100:.1f}%" for s in skill_scores],
        "Final Score (%)": final_scores,
        "Status":          ["✅ SHORTLISTED" if s >= SHORTLIST_THRESHOLD
                            else "❌ REJECTED" for s in final_scores],
        "Matched Skills":  matched_skills_list,
        "Missing Skills":  missing_skills_list,
    })
    df = df.sort_values("Final Score (%)", ascending=False).reset_index(drop=True)
    df.index += 1
    df.index.name = "Rank"
    return df

def save_report(df: pd.DataFrame, output_path: str = "outputs/screening_report.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"\n  ✅ Report saved → {output_path}")

def print_report(df: pd.DataFrame):
    try:
        from tabulate import tabulate
        display_df = df[["Name","TF-IDF Score","Skill Match","Final Score (%)","Status"]]
        print("\n" + "="*70)
        print("           AUTOMATED RESUME SCREENING RESULTS")
        print("="*70)
        print(tabulate(display_df, headers="keys", tablefmt="fancy_grid"))
    except ImportError:
        print(df[["Name","TF-IDF Score","Skill Match","Final Score (%)","Status"]].to_string())