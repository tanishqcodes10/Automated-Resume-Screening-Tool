"""
cleaner.py
Cleans and normalizes raw resume text for NLP processing.
"""
import re

STOPWORDS = {
    "i","me","my","we","our","you","your","he","him","his","she","her",
    "they","them","what","which","who","this","that","these","those","am",
    "is","are","was","were","be","been","being","have","has","had","do",
    "does","did","a","an","the","and","but","if","or","as","of","at","by",
    "for","with","in","out","on","off","to","from","up","not","can","will",
    "just","now","so","than","too","very","s","t","d","ll","m","re","ve"
}

def clean_text(text: str) -> str:
    """Full cleaning pipeline: lowercase → remove noise → remove stopwords"""
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)           # remove emails
    text = re.sub(r'http\S+|www\S+', ' ', text)    # remove URLs
    text = re.sub(r'\+?\d[\d\s\-\(\)]{7,}', ' ', text)  # remove phones
    text = re.sub(r'[^\w\s]', ' ', text)            # remove punctuation
    text = re.sub(r'\d+', ' ', text)               # remove numbers
    text = re.sub(r'\s+', ' ', text).strip()        # normalize spaces
    tokens = [w for w in text.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(tokens)

def extract_keywords(text: str) -> list:
    """Return sorted unique keywords from cleaned text."""
    return sorted(set(clean_text(text).split()))