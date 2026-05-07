import os
import sys
import tempfile
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.extractor import extract_resume_text
from src.scorer    import compute_tfidf_scores, compute_skill_scores, compute_final_scores
from src.reporter  import build_report, SHORTLIST_THRESHOLD

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Automated Resume Screening Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title  { font-size:2.2rem; font-weight:700; color:#01696f; margin-bottom:0; }
    .sub-title   { font-size:1rem; color:#7a7974; margin-top:0; margin-bottom:1.5rem; }
    .metric-card { background:#f9f8f5; border:1px solid #dcd9d5;
                   border-radius:0.75rem; padding:1rem 1.5rem; text-align:center; }
    .shortlisted { background:#d4dfcc; color:#1e3f0a;
                   padding:0.25rem 0.75rem; border-radius:999px;
                   font-weight:600; font-size:0.85rem; }
    .rejected    { background:#e0ced7; color:#561740;
                   padding:0.25rem 0.75rem; border-radius:999px;
                   font-weight:600; font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown('<p class="main-title">📄 Automated Resume Screening Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload resumes, define a job description, and let AI rank candidates instantly.</p>', unsafe_allow_html=True)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    st.subheader("1. Job Description")
    jd_input = st.text_area(
        "Paste the Job Description",
        value=open("data/job_description.txt").read() if os.path.exists("data/job_description.txt") else "",
        height=250,
        help="Paste the full job description here."
    )

    st.subheader("2. Required Skills")
    skills_default = open("data/required_skills.txt").read() if os.path.exists("data/required_skills.txt") else ""
    skills_input = st.text_area(
        "Enter required skills (one per line)",
        value=skills_default,
        height=200,
        help="Enter each required skill on a new line."
    )

    st.subheader("3. Scoring Weights")
    tfidf_weight = st.slider("TF-IDF Weight", 0.0, 1.0, 0.5, 0.1)
    skill_weight = round(1.0 - tfidf_weight, 1)
    st.info(f"Skill Match Weight: **{skill_weight}**")

    st.subheader("4. Shortlist Threshold")
    threshold = st.slider("Minimum Score to Shortlist (%)", 10, 90, 50, 5)

    run_btn = st.button("🚀 Run Screening", type="primary", use_container_width=True)

# ── Upload Resumes ────────────────────────────────────────────
st.subheader("📤 Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, or TXT resume files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="You can upload multiple resumes at once."
)

# Also offer to use sample resumes from /resumes folder
use_sample = st.checkbox(
    "✅ Also include sample resumes from the `resumes/` folder",
    value=True if not uploaded_files else False
)

# ── Run Pipeline ──────────────────────────────────────────────
if run_btn:
    if not jd_input.strip():
        st.error("⚠️ Please enter a Job Description in the sidebar.")
        st.stop()

    required_skills = [s.strip() for s in skills_input.strip().split("\n") if s.strip()]
    if not required_skills:
        st.error("⚠️ Please enter at least one required skill.")
        st.stop()

    # Collect resume texts
    names, filenames, resume_texts = [], [], []

    # From uploaded files
    if uploaded_files:
        with st.spinner("Extracting text from uploaded resumes..."):
            for uf in uploaded_files:
                suffix = os.path.splitext(uf.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uf.read())
                    tmp_path = tmp.name
                text = extract_resume_text(tmp_path)
                os.unlink(tmp_path)
                if text.strip():
                    name = os.path.splitext(uf.name)[0].replace("_", " ").title().replace("Resume ", "")
                    names.append(name)
                    filenames.append(uf.name)
                    resume_texts.append(text)

    # From sample resumes folder
    if use_sample and os.path.exists("resumes"):
        with st.spinner("Loading sample resumes..."):
            for fname in sorted(os.listdir("resumes")):
                if fname.lower().endswith((".txt", ".pdf", ".docx")):
                    fpath = os.path.join("resumes", fname)
                    text = extract_resume_text(fpath)
                    if text.strip():
                        name = os.path.splitext(fname)[0].replace("_", " ").title().replace("Resume ", "")
                        names.append(name)
                        filenames.append(fname)
                        resume_texts.append(text)

    if not resume_texts:
        st.error("⚠️ No valid resumes found. Please upload files or add samples to resumes/ folder.")
        st.stop()

    # Compute scores
    with st.spinner("Computing TF-IDF Cosine Similarity..."):
        tfidf_scores = compute_tfidf_scores(resume_texts, jd_input)
    with st.spinner("Computing Skill Match scores..."):
        skill_scores = compute_skill_scores(resume_texts, required_skills)
    final_scores = compute_final_scores(tfidf_scores, skill_scores, tfidf_weight, skill_weight)

    # Build report with dynamic threshold
    import src.reporter as rep_mod
    original_threshold = rep_mod.SHORTLIST_THRESHOLD
    rep_mod.SHORTLIST_THRESHOLD = threshold
    df = build_report(names, filenames, tfidf_scores, skill_scores,
                      final_scores, required_skills, resume_texts)
    rep_mod.SHORTLIST_THRESHOLD = original_threshold

    # ── Metrics ──────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Screening Summary")
    shortlisted = df[df["Status"] == "✅ SHORTLISTED"]
    rejected    = df[df["Status"] == "❌ REJECTED"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Resumes", len(df))
    col2.metric("Shortlisted ✅", len(shortlisted))
    col3.metric("Rejected ❌", len(rejected))
    col4.metric("Top Score", f"{df['Final Score (%)'].max()}%")

    # ── Results Table ─────────────────────────────────────────
    st.divider()
    st.subheader("🏆 Ranked Candidates")

    display_df = df[["Name", "TF-IDF Score", "Skill Match",
                     "Final Score (%)", "Status"]].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=False)

    # ── Score Bar Chart ───────────────────────────────────────
    st.divider()
    st.subheader("📈 Score Comparison")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(figsize=(10, max(4, len(df) * 0.7)))
    colors = ["#437a22" if s == "✅ SHORTLISTED" else "#a12c7b" for s in df["Status"]]
    bars = ax.barh(df["Name"], df["Final Score (%)"], color=colors, edgecolor="white", height=0.6)
    ax.axvline(x=threshold, color="#da7101", linestyle="--", linewidth=2, label=f"Threshold ({threshold}%)")
    ax.set_xlabel("Final Score (%)", fontsize=12)
    ax.set_title("Resume Screening Scores", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 100)

    for bar, score in zip(bars, df["Final Score (%)"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{score}%", va="center", fontsize=10)

    green_patch = mpatches.Patch(color="#437a22", label="Shortlisted")
    purple_patch = mpatches.Patch(color="#a12c7b", label="Rejected")
    ax.legend(handles=[green_patch, purple_patch, ax.get_lines()[0]], loc="lower right")
    plt.tight_layout()
    st.pyplot(fig)

    # ── Skill Match Detail ────────────────────────────────────
    st.divider()
    st.subheader("🔍 Skill Match Detail")
    skill_df = df[["Name", "Matched Skills", "Missing Skills", "Final Score (%)"]].copy()
    st.dataframe(skill_df, use_container_width=True, hide_index=False)

    # ── Shortlisted Section ───────────────────────────────────
    if not shortlisted.empty:
        st.divider()
        st.subheader("✅ Shortlisted Candidates")
        for _, row in shortlisted.iterrows():
            with st.expander(f"🏅 {row['Name']} — {row['Final Score (%)']}%"):
                c1, c2, c3 = st.columns(3)
                c1.metric("TF-IDF Score", row["TF-IDF Score"])
                c2.metric("Skill Match", row["Skill Match"])
                c3.metric("Final Score", f"{row['Final Score (%)']}%")
                st.write(f"**Matched Skills:** {row['Matched Skills']}")
                if row["Missing Skills"] != "None":
                    st.write(f"**Missing Skills:** {row['Missing Skills']}")

    # ── Download Report ───────────────────────────────────────
    st.divider()
    csv_data = df.to_csv().encode("utf-8")
    st.download_button(
        label="⬇️ Download Full Report as CSV",
        data=csv_data,
        file_name="screening_report.csv",
        mime="text/csv",
        type="primary"
    )

else:
    st.info("👈 Configure settings in the sidebar and click **Run Screening** to start.")
    with st.expander("ℹ️ How This Tool Works"):
        st.markdown("""
**Workflow:**
1. **Upload Resumes** (.txt, .pdf, or .docx files)
2. **Paste Job Description** in the sidebar
3. **List Required Skills** (one per line)
4. **Adjust Weights** for TF-IDF vs. Skill Match scoring
5. **Click Run Screening** — results appear instantly

**Scoring Method:**
- **TF-IDF Cosine Similarity** — how semantically similar is the resume to the JD?
- **Skill Match %** — what % of required skills are found in the resume?
- **Final Score** = TF-IDF Weight × TF-IDF Score + Skill Weight × Skill Score
        """)