import re
from utils import preprocess_text
# Predefined Skills to check
SKILL_DB = [
    "python", "java", "c++", "sql",
    "machine learning", "deep learning",
    "pandas", "numpy",
    "tensorflow", "pytorch",
    "docker", "aws", "git",
    "linux", "flask", "fastapi",
    "nlp", "opencv",
    "excel", "power bi", "tableau",
    "statistics", "data analysis",
    "machine learning", "deep learning",
    "rest api", "mongodb", "mysql","devops"
]

def extract_skills(text):
    """
    Extract skills using dictionary-based matching
    """
    text = preprocess_text(text)

    found_skills = set()

    for skill in SKILL_DB:
        if skill in text:
            found_skills.add(skill)

    return list(found_skills)


def get_matching_skills(resume_skills, jd_skills):
    """Common skills"""
    return list(set(resume_skills) & set(jd_skills))


def get_missing_skills(resume_skills, jd_skills):
    """Skills present in JD but missing in resume"""
    return list(set(jd_skills) - set(resume_skills))