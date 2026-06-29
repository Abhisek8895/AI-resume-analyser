import re
from utils import preprocess_text

SKILL_DB = [
    "python", "java", "c++", "c#", "sql",
    "machine learning", "deep learning",
    "pandas", "numpy",
    "tensorflow", "pytorch",
    "docker", "aws", "git",
    "linux", "flask", "fastapi",
    "nlp", "opencv",
    "excel", "power bi", "tableau",
    "statistics", "data analysis",
    "rest api", "mongodb", "mysql", "devops",
]


def _build_pattern(skill):
    """
    Build a word-boundary-safe regex for a skill so substrings don't
    falsely match.
    """
    escaped = re.escape(skill)

    if any(ch in skill for ch in ["+", "#"]):
        pattern = r"(?<![^\s]){}(?![^\s])".format(escaped)
    else:
        pattern = r"\b{}\b".format(escaped)

    return re.compile(pattern)

_SKILL_PATTERNS = {skill: _build_pattern(skill) for skill in SKILL_DB}


def extract_skills(text):
    """
    Extract skills using dictionary-based matching with word boundaries
    """
    text = preprocess_text(text)
    found_skills = set()

    for skill, pattern in _SKILL_PATTERNS.items():
        if pattern.search(text):
            found_skills.add(skill)

    return list(found_skills)


def get_matching_skills(resume_skills, jd_skills):
    """Skills present in both resume and JD."""
    return list(set(resume_skills) & set(jd_skills))


def get_missing_skills(resume_skills, jd_skills):
    """Skills present in JD but missing from resume."""
    return list(set(jd_skills) - set(resume_skills))