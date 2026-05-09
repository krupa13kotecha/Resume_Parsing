import sys
import pdfplumber
import json
import pickle

# Load trained model
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except:
    model = None
    vectorizer = None
def get_ml_prediction(text):
    if model is None or vectorizer is None:
        return "Unknown", 0

    vec = vectorizer.transform([text])
    category = model.predict(vec)[0]

    # simple score mapping (you can improve later)
    category_scores = {
        "Data Science": 90,
        "Engineering": 85,
        "HR": 70,
        "Finance": 75
    }

    ai_score = category_scores.get(category, 60)

    return category, ai_score
def extract_text(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except:
        text = ""
    return text

skills_db = [
    "python", "java", "c++", "c", "html", "css", "javascript",
    "react", "node", "mongodb", "sql", "mysql",
    "git", "github", "linux", "aws"
]

keywords_db = [
    "project", "projects", "experience", "internship",
    "developed", "built", "designed", "implemented",
    "team", "leadership", "managed", "achieved",
    "responsible", "collaborated"
]

def extract_skills(text):
    found_skills = []
    text_lower = text.lower()

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))

def keyword_score(text):
    count = 0
    text_lower = text.lower()

    for word in keywords_db:
        if word in text_lower:
            count += 1

    score = (count / len(keywords_db)) * 100
    return round(score, 2)


def structure_score(text):
    sections = ["education", "skills", "projects", "experience"]

    found = 0
    text_lower = text.lower()

    for sec in sections:
        if sec in text_lower:
            found += 1

    score = (found / len(sections)) * 100
    return round(score, 2)


def skill_score(skills):
    total_skills = 10
    score = (len(skills) / total_skills) * 100
    return round(score, 2)


def final_score(skill_s, keyword_s, structure_s):
    return round(
        (0.5 * skill_s) +
        (0.3 * keyword_s) +
        (0.2 * structure_s),
        2
    )

if __name__ == "__main__":
    file_path = sys.argv[1]

    text = extract_text(file_path)

    skills = extract_skills(text)
    skill_s = skill_score(skills)
    keyword_s = keyword_score(text)
    structure_s = structure_score(text)

    ats_score = final_score(skill_s, keyword_s, structure_s)
    theoretical_score = final_score(skill_s, keyword_s, structure_s)
    ml_category, ai_score = get_ml_prediction(text)
    final_score_combined = round(
    (0.5 * theoretical_score) + (0.5 * ai_score), 2
)
    result = {
    "skills": skills,

    "theoretical_score": theoretical_score,   # rule-based
    "ai_score": ai_score,                     # ML-based
    "final_score": final_score_combined,      # hybrid

    "ml_category": ml_category,

    "breakdown": {
        "skill_score": skill_s,
        "keyword_score": keyword_s,
        "structure_score": structure_s
    }
}

    print(json.dumps(result))