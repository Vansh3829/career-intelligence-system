import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = ["python", "sql", "machine learning", "data analysis",
             "java", "cloud", "statistics", "deep learning"]

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.lower()

def extract_skills(text):
    return list({skill for skill in SKILLS_DB if skill in text})

def extract_experience_years(text):
    # simple heuristic
    if "year" in text:
        return min(10, max(1, text.count("year")))
    return 1
