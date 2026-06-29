import streamlit as st
from PyPDF2 import PdfReader

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

from utils import preprocess_text
from analyzer import calculate_similarity,get_ats_grade,get_ats_feedback
from skills import extract_skills,get_matching_skills,get_missing_skills

# Title
st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF only)",
    type=["pdf"]
)


# Function to extract PDF text
def extract_pdf_text(file):

    pdf_reader = PdfReader(file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


# Main logic
if uploaded_file is not None:

    # Get file extension
    file_type = uploaded_file.name.split(".")[-1].lower()

    # Extract text
    if file_type == "pdf":
        resume_text = extract_pdf_text(uploaded_file)

    else:
        st.error(
            f"'.{file_type}' files are not supported yet. "
            "Please upload a PDF resume."
        )
        st.stop()

    # Success message
    st.success("Resume parsed successfully ✅")

    # Job description input
    job_description = st.text_area(
        "Paste Job Description",
        height=200
    )

    # Analyze button
    if st.button("Analyze Resume"):

        if job_description.strip() == "":
            st.warning("Please enter a job description.")

        else:
            # st.write("Analysis will start here...")
            score = calculate_similarity(resume_text,job_description)
            grade = get_ats_grade(score)
            feedback = get_ats_feedback(score)

            st.metric("ATS Score", f"{score:.2f}%")

            st.success(f"Grade: {grade}")

            st.info(feedback)

            clean_resume = preprocess_text(resume_text)
            clean_jd = preprocess_text(job_description)

            resume_skills = extract_skills(clean_resume)
            jd_skills = extract_skills(clean_jd)

            matched_skills = get_matching_skills(resume_skills, jd_skills)
            missing_skills = get_missing_skills(resume_skills, jd_skills)

            st.subheader("🧠 Skills Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"Matched Skills ({len(matched_skills)}):\n\n"
                    + ", ".join(skill.title() for skill in matched_skills)
                )

            with col2:
                st.write(
                    f"Missing Skills ({len(missing_skills)}):\n\n"
                    + ", ".join(skill.title() for skill in missing_skills)
                )