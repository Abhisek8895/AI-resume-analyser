import re

def preprocess_text(text):
    """
    Clean text for matching/embedding while preserving characters
    that matter for tech skill names.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#\.]", " ", text)

    # Collapse repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()