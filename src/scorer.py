"""
scorer.py
TF-IDF vectorization + Cosine Similarity + Skill Match scoring.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.cleaner import clean_text

def compute_tfidf_scores(resume_texts: list, jd_text: str) -> list:
    """Compute cosine similarity between each resume and the job description."""
    corpus = [jd_text] + resume_texts
    cleaned_corpus = [clean_text(doc) for doc in corpus]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),   # unigrams + bigrams
        max_features=5000,
        sublinear_tf=True     # log normalization
    )
    tfidf_matrix = vectorizer.fit_transform(cleaned_corpus)
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]
    scores = cosine_similarity(jd_vector, resume_vectors)[0]
    return [round(float(s), 4) for s in scores]

def compute_skill_scores(resume_texts: list, required_skills: list) -> list:
    """Calculate % of required skills found in each resume."""
    skill_scores = []
    required_lower = [s.lower().strip() for s in required_skills]
    for text in resume_texts:
        text_lower = text.lower()
        matched = sum(1 for skill in required_lower if skill in text_lower)
        score = matched / len(required_lower) if required_lower else 0.0
        skill_scores.append(round(score, 4))
    return skill_scores

def compute_final_scores(tfidf_scores: list, skill_scores: list,
                         tfidf_weight: float = 0.5,
                         skill_weight: float = 0.5) -> list:
    """Combine TF-IDF and skill scores into a weighted final score (0–100)."""
    final = []
    for t, s in zip(tfidf_scores, skill_scores):
        score = (t * tfidf_weight + s * skill_weight) * 100
        final.append(round(score, 2))
    return final