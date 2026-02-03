SKILL_WEIGHTS = {
    "python": 3,
    "sql": 3,
    "machine learning": 4,
    "data analysis": 3,
    "statistics": 4,
    "cloud": 2
}

def compute_skill_score(skills):
    return sum(SKILL_WEIGHTS.get(skill, 1) for skill in skills)
