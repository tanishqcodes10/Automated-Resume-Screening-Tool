# 📄 Automated Resume Screening Tool

> **An intelligent Python-based ATS simulation that ranks and shortlists resumes using TF-IDF Cosine Similarity and Keyword Skill Matching.**


***

## 📌 Problem Statement

Companies receive hundreds of resumes for every open position. Manual screening is:
- **Time-consuming** (HR teams spend 23 seconds on average per resume)
- **Inconsistent** (human bias affects decisions)
- **Expensive** (wastes recruiter hours on unqualified candidates)

This project simulates an **Applicant Tracking System (ATS)** that automatically screens, scores, and ranks resumes against a job description using NLP techniques.

***

## 🏭 Industry Relevance

| Industry | Application |
|----------|-------------|
| HR Tech | Automate initial resume shortlisting |
| Recruitment | Build smarter candidate pipelines |
| AI/NLP | Real-world text similarity application |
| Data Analytics | Candidate scoring and ranking reports |
| Python Development | Modular, production-ready Python code |

***

## ✨ Features

- ✅ **Multi-format support**: PDF, DOCX, and TXT resume parsing
- ✅ **TF-IDF Vectorization** with bigrams for semantic similarity
- ✅ **Cosine Similarity** scoring (resume vs. job description)
- ✅ **Skill Match Percentage** — exact keyword matching
- ✅ **Weighted Final Score** — combine both methods
- ✅ **Ranked Results Table** — best candidates at the top
- ✅ **Shortlist/Reject Decision** — configurable threshold
- ✅ **CSV Report Generation** — ready for HR teams
- ✅ **Streamlit Dashboard** — interactive web interface
- ✅ **Matched & Missing Skills** per candidate

***

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| PDF Extraction | pdfplumber, PyPDF2 |
| DOCX Extraction | python-docx |
| Data Processing | Pandas, NumPy |
| NLP / ML | Scikit-learn (TF-IDF, Cosine Similarity) |
| Web Dashboard | Streamlit |
| Visualization | Matplotlib |
| Reporting | CSV (Pandas) |
| Version Control | Git, GitHub |

***

## 🗂️ Folder Structure

```
Automated-Resume-Screening-Tool/
│
├── resumes/                  ← Sample resume files (.txt, .pdf, .docx)
│   ├── resume_alice.txt
│   ├── resume_bob.txt
│   ├── resume_carol.txt
│   ├── resume_david.txt
│   └── resume_eva.txt
│
├── data/                     ← Input configuration files
│   ├── job_description.txt   ← Paste job description here
│   └── required_skills.txt   ← One skill per line
│
├── src/                      ← Core Python modules
│   ├── __init__.py
│   ├── extractor.py          ← PDF/DOCX/TXT text extraction
│   ├── cleaner.py            ← Text cleaning & preprocessing
│   ├── scorer.py             ← TF-IDF + Cosine Similarity scoring
│   └── reporter.py           ← CSV report generation
│
├── outputs/                  ← Generated reports
│   └── screening_report.csv
│
├── images/                   ← Screenshots for documentation
├── docs/                     ← Additional documentation
│
├── main.py                   ← 🚀 CLI entry point
├── app.py                    ← 🌐 Streamlit dashboard
├── requirements.txt          ← Python dependencies
├── .gitignore
└── README.md
```

***

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Automated-Resume-Screening-Tool.git
cd Automated-Resume-Screening-Tool
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Tool (CLI)
```bash
python main.py
```

### 5. Run the Streamlit Dashboard (Optional)
```bash
streamlit run app.py
```
Then open: **http://localhost:8501**

***

## 📁 How to Use

### Step 1: Add Your Resumes
Place resume files (`.txt`, `.pdf`, or `.docx`) inside the `resumes/` folder.

### Step 2: Edit the Job Description
Open `data/job_description.txt` and paste the job description you want to screen against.

### Step 3: Edit Required Skills
Open `data/required_skills.txt` and list one required skill per line.

### Step 4: Run
```bash
python main.py
```

***

## 📊 Sample Output

```
============================================================
     AUTOMATED RESUME SCREENING TOOL
============================================================

[1/5] Loading job description and required skills...
  ✅ Job Description loaded (104 words)
  ✅ Required Skills loaded: 18 skills

[2/5] Loading resumes from 'resumes/' ...
  📄 Extracting: resume_alice.txt
  📄 Extracting: resume_carol.txt
  📄 Extracting: resume_eva.txt
  📄 Extracting: resume_bob.txt
  📄 Extracting: resume_david.txt

[5/5] Generating report...

╒════════╤════════╤════════════════╤═══════════════╤═══════════════════╤════════════════╕
│   Rank │ Name   │ TF-IDF Score   │ Skill Match   │   Final Score (%) │ Status         │
╞════════╪════════╪════════════════╪═══════════════╪═══════════════════╪════════════════╡
│      1 │ Alice  │ 20.3%          │ 100.0%        │             60.15 │ ✅ SHORTLISTED │
│      2 │ Carol  │ 17.5%          │ 100.0%        │             58.77 │ ✅ SHORTLISTED │
│      3 │ Eva    │ 15.9%          │ 88.9%         │             52.39 │ ✅ SHORTLISTED │
│      4 │ Bob    │ 3.9%           │ 27.8%         │             15.85 │ ❌ REJECTED    │
│      5 │ David  │ 2.1%           │ 16.7%         │              9.39 │ ❌ REJECTED    │
╘════════╧════════╧════════════════╧═══════════════╧═══════════════════╧════════════════╝

  📊 Total Resumes Screened : 5
  ✅ Shortlisted            : 3
  ❌ Rejected               : 2
  🏆 Top Candidate          : Alice (60.15%)
============================================================
```

***

## 🧮 Scoring Algorithm

```
Final Score = (TF-IDF_Weight × TF-IDF_Score) + (Skill_Weight × Skill_Match_Score)
```

| Component | Default Weight | Method |
|-----------|---------------|--------|
| TF-IDF Cosine Similarity | 50% | Bigram TF-IDF → Cosine Similarity |
| Skill Match % | 50% | Keyword presence check |
| **Final Score** | **100%** | **Weighted combination** |

Candidates scoring **≥ 50%** are **SHORTLISTED**. All others are **REJECTED**.

***

## 📈 Workflow

```
Resume Files (.txt/.pdf/.docx)
        ↓
  Text Extraction (pdfplumber / python-docx)
        ↓
  Text Cleaning (lowercase, remove noise, stopwords)
        ↓
  TF-IDF Vectorization (sklearn)
        ↓
  Cosine Similarity Score (vs. Job Description)
        ↓
  Skill Match Score (keyword overlap)
        ↓
  Weighted Final Score (50% + 50%)
        ↓
  Ranking + Shortlist / Reject Decision
        ↓
  CSV Report + Streamlit Dashboard
```

***

## 🎓 Learning Outcomes

By building this project, you will learn:
- Text extraction from real-world file formats (PDF, DOCX, TXT)
- NLP preprocessing: tokenization, stopword removal, normalization
- TF-IDF vectorization and how it weighs word importance
- Cosine similarity for document comparison
- Building modular Python applications
- Generating business-ready CSV reports with Pandas
- Creating interactive dashboards with Streamlit
- Real-world ATS workflow simulation

***

## 👤 Author

 Tanishq Jakate
🔗 [LinkedIn](linkedin.com/in/tanishq-jakate-93617a402) | 
    [GitHub](https://github.com/tanishqcodes10)

***

***

## ⭐ If this helped you, please give it a star!
