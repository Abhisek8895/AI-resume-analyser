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

# Title
st.title("AI Resume Analyzer")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Your Resume",
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
    file_type = uploaded_file.name.split(".")[-1]

    # Extract text
    if file_type == "pdf":
        resume_text = extract_pdf_text(uploaded_file)

    else:
        resume_text = ""

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
            clean_resume = preprocess_text(resume_text)
            clean_jd = preprocess_text(job_description)

            score = calculate_similarity(clean_resume, clean_jd)
            grade = get_ats_grade(score)
            feedback = get_ats_feedback(score)

            st.metric("ATS Score", f"{score:.2f}%")

            st.success(f"Grade: {grade}")

            st.info(feedback)