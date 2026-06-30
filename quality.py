import re

WEAK_VERBS = {
    "worked on": ["Built", "Developed", "Implemented"],
    "helped with": ["Contributed to", "Drove", "Supported"],
    "helped": ["Contributed to", "Drove", "Supported"],
    "responsible for": ["Led", "Managed", "Owned"],
    "involved in": ["Participated in", "Drove", "Contributed to"],
    "assisted in": ["Supported", "Facilitated", "Contributed to"],
    "assisted with": ["Supported", "Facilitated", "Contributed to"],
    "tasked with": ["Led", "Owned", "Drove"],
    "in charge of": ["Led", "Managed", "Directed"],
    "participated in": ["Contributed to", "Drove", "Collaborated on"],
    "did": ["Executed", "Performed", "Completed"],
    "made": ["Built", "Created", "Developed"],
}

# Sort by phrase length 
_SORTED_WEAK_VERBS = sorted(WEAK_VERBS.items(), key=lambda kv: -len(kv[0]))

# Quantification: looks for digits, optionally followed by %, +, x,
QUANTIFICATION_PATTERN = re.compile(
    r"\d+[,.]?\d*\s*(%|\+|x|k|m|million|billion|hours?|days?|years?|"
    r"users?|customers?|dollars?|\$)?",
    re.IGNORECASE,
)


def _find_weak_verb(bullet_text):
    cleaned = bullet_text.strip().lower()
    # Strip a leading bullet marker like "-", "•", "*" if present
    cleaned = re.sub(r"^[\-\*•]\s*", "", cleaned)

    for phrase, suggestions in _SORTED_WEAK_VERBS:
        # Check if the bullet STARTS with this phrase (most common
        # spot for a weak verb) using a word-boundary-safe check.
        pattern = r"^\b" + re.escape(phrase) + r"\b"
        if re.match(pattern, cleaned):
            return phrase, suggestions

    return None, None


def has_quantification(bullet_text):
    """Return True if the bullet contains a number/metric."""
    return bool(re.search(r"\d", bullet_text))


def analyze_bullet(bullet_text):
    """
    Analyze a single bullet point.
    """
    weak_verb, suggestions = _find_weak_verb(bullet_text)
    return {
        "text": bullet_text.strip(),
        "weak_verb": weak_verb,
        "suggestions": suggestions,
        "has_metric": has_quantification(bullet_text),
    }


def extract_bullets(section_text):
    """
    Split a section's text into individual bullet points.
    """
    lines = section_text.split("\n")
    bullets = []
    for line in lines:
        stripped = line.strip()
        if stripped and stripped.startswith(("-", "•", "*")):
            bullets.append(stripped)
    return bullets


def analyze_section(section_text):
    """
    Run analyze_bullet() on every bullet point in a section.
    """
    bullets = extract_bullets(section_text)
    return [analyze_bullet(b) for b in bullets]