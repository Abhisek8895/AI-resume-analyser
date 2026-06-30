import re

SECTION_ALIASES = {
    "experience": [
        "experience", "work experience","workexperience", "professional experience",
         "professionalexperience", "employment history", "employmenthistory",
           "workhistory", "career history", "careerhistory",
    ],
    "education": [
        "education", "academic background","academicbackground", "educational qualifications",
        "academic qualifications", "educationalqualifications","academicqualifications",
    ],
    "skills": [
        "skills", "technical skills", "key skills", "core competencies",
        "skill set","skillset", "competencies","corecompetencies","keyskills","technicalskills",
    ],
    "projects": [
        "projects", "personal projects", "academic projects",
        "key projects", "personalprojects", "academicprojects","keyprojects",
    ],
    "certifications": [
        "certifications", "certificates", "licenses & certifications", "licenses&certifications",
    ],
    "summary": [
        "summary", "professional summary", "career summary", "careersummary",
        "profile", "objective", "career objective","professionalsummary", "profile summary",
        "profilesummary", "careerobjective",
    ],
}

REQUIRED_SECTIONS = ["experience", "education", "skills","summary"]

MAX_HEADING_WORDS = 4


def _clean_line(line):
    """Lowercase, strip whitespace, and remove common heading
    decorations like dashes/colons/stars around the text."""
    line = line.strip().lower()
    # strip leading/trailing decoration characters: -, *, :, •, —, etc.
    line = re.sub(r"^[\s\-\*:•—_]+|[\s\-\*:•—_]+$", "", line)
    return line.strip()


def _match_heading(cleaned_line):
    no_space_line = cleaned_line.replace(" ", "")

    for canonical, aliases in SECTION_ALIASES.items():
        if cleaned_line in aliases:
            return canonical
        # Fallback: compare with spaces stripped from both sides
        if any(no_space_line == alias.replace(" ", "") for alias in aliases):
            return canonical

    return None

def detect_sections(resume_text):
    """
    Split resume_text into sections.
    """
    lines = resume_text.split("\n")

    sections = {}
    current_section = "header"
    buffer = []

    for raw_line in lines:
        cleaned = _clean_line(raw_line)
        word_count = len(cleaned.split())

        is_short = 0 < word_count <= MAX_HEADING_WORDS
        matched_section = _match_heading(cleaned) if is_short else None

        if matched_section:
            # Save whatever we've buffered for the previous section
            if buffer:
                sections[current_section] = sections.get(current_section, "") + "\n".join(buffer)
            buffer = []
            current_section = matched_section
        else:
            if raw_line.strip():
                buffer.append(raw_line.strip())

    # Flush whatever's left in the buffer at the end of the loop
    if buffer:
        sections[current_section] = sections.get(current_section, "") + "\n".join(buffer)

    return sections


def check_required_sections(sections):
    """
    Compare detected sections against REQUIRED_SECTIONS.
    """
    found = [s for s in REQUIRED_SECTIONS if s in sections and sections[s].strip()]
    missing = [s for s in REQUIRED_SECTIONS if s not in found]
    return found, missing