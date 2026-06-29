import re

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

PHONE_PATTERN = re.compile(
    r"(\+?\d{1,3}[\s.-]?)?(\(?\d{2,4}\)?[\s.-]?){1,4}\d{3,4}"
)


def find_email(text):
    """Return the first email address found in text, or None."""
    match = EMAIL_PATTERN.search(text)
    return match.group() if match else None


def find_phone(text):
    """Return the first phone number found in text, or None."""
    match = PHONE_PATTERN.search(text)
    return match.group().strip() if match else None


def check_contact_info(text):
    """
    Check resume text for contact info.

    Returns a dict:
        {
            "email": "john@example.com" or None,
            "phone": "+1-555-123-4567" or None,
            "has_contact_info": True/False  (True if at least one found)
        }
    """
    email = find_email(text)
    phone = find_phone(text)

    return {
        "email": email,
        "phone": phone,
        "has_contact_info": bool(email or phone),
    }