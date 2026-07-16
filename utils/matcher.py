def star_rating(score):
    if score >= 90:
        filled, label = 5, "Excellent Match"
    elif score >= 75:
        filled, label = 4, "Good Match"
    elif score >= 60:
        filled, label = 3, "Average Match"
    elif score >= 40:
        filled, label = 2, "Weak Match"
    else:
        filled, label = 1, "Poor Match"

    return {"filled": filled, "empty": 5 - filled, "label": label}


def fit_status(score):
    if score >= 75:
        return {"label": "Strong Fit", "css": "success"}
    if score >= 60:
        return {"label": "Moderate Fit", "css": "primary"}
    if score >= 40:
        return {"label": "Weak Fit", "css": "warning"}
    return {"label": "Not a Fit", "css": "danger"}


def skill_coverage(matched_skills, missing_skills):
    total = len(matched_skills) + len(missing_skills)
    if total == 0:
        return 0
    return round(len(matched_skills) / total * 100)
