import os
import sys

# ── Add project root to path ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.extractor import extract_resume_text
from src.scorer    import compute_tfidf_scores, compute_skill_scores, compute_final_scores
from src.reporter  import build_report, save_report, print_report

# ── Configuration ─────────────────────────────────────────────
RESUME_FOLDER      = "resumes"
JD_FILE            = "data/job_description.txt"
SKILLS_FILE        = "data/required_skills.txt"
OUTPUT_CSV         = "outputs/screening_report.csv"
SUPPORTED_FORMATS  = (".txt", ".pdf", ".docx")

# Scoring weights (must sum to 1.0)
TFIDF_WEIGHT  = 0.5
SKILL_WEIGHT  = 0.5


def load_text_file(path: str) -> str:
    """Read a plain text file and return its content."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_skills_list(path: str) -> list:
    """Read required skills from a file, one skill per line."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        skills = [line.strip() for line in f if line.strip()]
    return skills


def load_resumes(folder: str) -> tuple:
    """
    Scan the resume folder and load all supported files.
    Returns: (names, filenames, texts)
    """
    names, filenames, texts = [], [], []
    files = sorted(os.listdir(folder))

    for fname in files:
        if not fname.lower().endswith(SUPPORTED_FORMATS):
            continue
        fpath = os.path.join(folder, fname)
        print(f"  📄 Extracting: {fname}")
        text = extract_resume_text(fpath)

        if text.strip():
            # Derive a display name from filename
            name = os.path.splitext(fname)[0].replace("_", " ").title()
            # Remove common prefixes like "Resume "
            name = name.replace("Resume ", "").strip()
            names.append(name)
            filenames.append(fname)
            texts.append(text)
        else:
            print(f"  [!] Skipping {fname} — no text extracted.")

    return names, filenames, texts


def main():
    print("\n" + "="*60)
    print("     AUTOMATED RESUME SCREENING TOOL")
    print("="*60)

    # ── Step 1: Load inputs ───────────────────────────────────
    print("\n[1/5] Loading job description and required skills...")
    if not os.path.exists(JD_FILE):
        print(f"  [ERROR] Job description not found: {JD_FILE}")
        sys.exit(1)
    if not os.path.exists(SKILLS_FILE):
        print(f"  [ERROR] Skills file not found: {SKILLS_FILE}")
        sys.exit(1)

    jd_text        = load_text_file(JD_FILE)
    required_skills = load_skills_list(SKILLS_FILE)
    print(f"  ✅ Job Description loaded ({len(jd_text.split())} words)")
    print(f"  ✅ Required Skills loaded: {len(required_skills)} skills")
    print(f"     → {', '.join(required_skills[:8])}{'...' if len(required_skills) > 8 else ''}")

    # ── Step 2: Load resumes ──────────────────────────────────
    print(f"\n[2/5] Loading resumes from '{RESUME_FOLDER}/' ...")
    if not os.path.exists(RESUME_FOLDER):
        print(f"  [ERROR] Resume folder not found: {RESUME_FOLDER}")
        sys.exit(1)

    names, filenames, resume_texts = load_resumes(RESUME_FOLDER)

    if not resume_texts:
        print("  [ERROR] No valid resumes found. Add .txt, .pdf, or .docx files to resumes/")
        sys.exit(1)

    print(f"\n  ✅ {len(resume_texts)} resumes loaded successfully.")

    # ── Step 3: Compute scores ────────────────────────────────
    print("\n[3/5] Computing TF-IDF Cosine Similarity scores...")
    tfidf_scores = compute_tfidf_scores(resume_texts, jd_text)

    print("[4/5] Computing Skill Match scores...")
    skill_scores = compute_skill_scores(resume_texts, required_skills)

    print(f"      Combining scores (TF-IDF {int(TFIDF_WEIGHT*100)}% + Skill {int(SKILL_WEIGHT*100)}%)...")
    final_scores = compute_final_scores(tfidf_scores, skill_scores, TFIDF_WEIGHT, SKILL_WEIGHT)

    # ── Step 4: Build & display report ───────────────────────
    print("\n[5/5] Generating report...")
    df = build_report(names, filenames, tfidf_scores, skill_scores,
                      final_scores, required_skills, resume_texts)
    print_report(df)

    # ── Step 5: Save CSV ──────────────────────────────────────
    save_report(df, OUTPUT_CSV)

    # ── Summary ───────────────────────────────────────────────
    shortlisted = df[df["Status"] == "✅ SHORTLISTED"]
    rejected    = df[df["Status"] == "❌ REJECTED"]

    print("\n" + "="*60)
    print(f"  📊 Total Resumes Screened : {len(df)}")
    print(f"  ✅ Shortlisted            : {len(shortlisted)}")
    print(f"  ❌ Rejected               : {len(rejected)}")
    print(f"  🏆 Top Candidate          : {df.iloc[0]['Name']} ({df.iloc[0]['Final Score (%)']}%)")
    print("="*60)
    print(f"\n  Report saved to: {OUTPUT_CSV}")
    print("  Run 'streamlit run app.py' for the interactive dashboard.\n")


if __name__ == "__main__":
    main()