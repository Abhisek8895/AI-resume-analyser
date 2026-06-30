import streamlit as st
from PyPDF2 import PdfReader

# page config must come before any other st call
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="◢",
    layout="wide"
)

from utils import preprocess_text
from analyzer import calculate_similarity,get_ats_grade,get_ats_feedback
from skills import extract_skills,get_matching_skills,get_missing_skills
from sections import detect_sections, check_required_sections, REQUIRED_SECTIONS
from contact import check_contact_info
from quality import analyze_section
from rewrite import rewrite_bullet

# dark terminal-inspired theme: near-black surfaces, monospace data, single green accent
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #0D1117;
    --surface: #161B22;
    --surface-2: #1C2128;
    --border: #30363D;
    --text: #E6EDF3;
    --text-dim: #8B949E;
    --accent: #39D353;
    --warn: #D29922;
    --warn-bg: #2B2111;
}

.stApp { background-color: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] { background-color: var(--surface); border-right: 1px solid var(--border); }
h1, h2, h3 { font-family: 'JetBrains Mono', monospace !important; font-weight: 500 !important; letter-spacing: -0.02em; }

/* the score readout is the signature element - terminal scan-line feel */
.scan-result {
    font-family: 'JetBrains Mono', monospace;
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 6px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.5rem;
}
.scan-label { color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }
.scan-score { font-size: 2.75rem; font-weight: 700; color: var(--accent); line-height: 1.1; }
.scan-grade { color: var(--text-dim); font-size: 0.95rem; margin-top: 0.25rem; }

/* status rows used for section/contact/skill/bullet checks */
.status-row { font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; padding: 0.4rem 0; border-bottom: 1px solid var(--surface-2); }
.status-pass { color: var(--accent); }
.status-warn { color: var(--warn); }
.status-detail { color: var(--text-dim); font-size: 0.82rem; font-family: 'Inter', sans-serif; margin: 0.15rem 0 0.5rem 1.4rem; }

.bullet-card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; }
.bullet-card.ok { border-left: 3px solid var(--accent); }
.bullet-card.flag { border-left: 3px solid var(--warn); }

div.stButton > button {
    background-color: var(--surface-2);
    color: var(--accent);
    border: 1px solid var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    border-radius: 4px;
}
div.stButton > button:hover { background-color: var(--accent); color: var(--bg); }

::placeholder { color: var(--text-dim) !important; opacity: 1; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# reusable renderer for a status row with optional dim detail line below it
def render_status(passed, label, detail=None):
    icon = "✓" if passed else "!"
    css_class = "status-pass" if passed else "status-warn"
    st.markdown(
        f'<div class="status-row {css_class}">[{icon}] {label}</div>',
        unsafe_allow_html=True
    )
    if detail:
        st.markdown(f'<div class="status-detail">{detail}</div>', unsafe_allow_html=True)


# extracts raw text from an uploaded pdf, page by page
def extract_pdf_text(file):

    pdf_reader = PdfReader(file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


# header
st.markdown(
    '<h1 style="margin-bottom:0;">◢ resume_analyzer</h1>'
    '<p style="color: var(--text-dim); font-family: \'JetBrains Mono\', monospace; '
    'font-size: 0.85rem; margin-top: 0.2rem;">// ats compatibility + JD match scanner</p>',
    unsafe_allow_html=True
)

# sidebar holds all inputs - upload and JD - keeping the main area free for results
with st.sidebar:
    st.markdown("### inputs")
    uploaded_file = st.file_uploader("resume (pdf only)", type=["pdf"])
    job_description = st.text_area("job description", height=220, placeholder="paste the JD here...")
    analyze_clicked = st.button("▶ run analysis", use_container_width=True)

# main logic
if uploaded_file is not None:

    # get file extension
    file_type = uploaded_file.name.split(".")[-1].lower()

    # extract text
    if file_type == "pdf":
        resume_text = extract_pdf_text(uploaded_file)

    else:
        st.error(
            f"'.{file_type}' files are not supported yet. "
            "Please upload a PDF resume."
        )
        st.stop()

    if not resume_text.strip():
        st.error(
            "Couldn't extract any text from this PDF. "
            "It might be a scanned/image-based resume rather than a "
            "text-based one. Please upload a text-based PDF."
        )
        st.stop()

    sections = detect_sections(resume_text)
    found_sections, missing_sections = check_required_sections(sections)
    contact_result = check_contact_info(resume_text)

    st.markdown("### structure check")

    for section in REQUIRED_SECTIONS:
        render_status(section in found_sections, f"{section} section")

    if contact_result["has_contact_info"]:
        contact_parts = []
        if contact_result["email"]:
            contact_parts.append(f"email: {contact_result['email']}")
        if contact_result["phone"]:
            contact_parts.append(f"phone: {contact_result['phone']}")
        render_status(True, "contact info", detail=", ".join(contact_parts))
    else:
        render_status(False, "contact info", detail="no email or phone detected near the top of the resume")

    st.markdown("<br>", unsafe_allow_html=True)

    # store the click so it survives reruns triggered by the rewrite buttons below
    if analyze_clicked:
        st.session_state["analyzed"] = True

    if st.session_state.get("analyzed"):

        if job_description.strip() == "":
            st.warning("Please enter a job description in the sidebar.")

        else:
            try:
                score = calculate_similarity(resume_text,job_description)
                grade = get_ats_grade(score)
                feedback = get_ats_feedback(score)

                # signature scan-result readout
                st.markdown(
                    f'<div class="scan-result">'
                    f'<div class="scan-label">match score</div>'
                    f'<div class="scan-score">{score:.1f}%<span style="color:var(--text-dim); '
                    f'font-size:1.5rem;">_</span></div>'
                    f'<div class="scan-grade">grade: {grade}  ·  {feedback}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                clean_resume = preprocess_text(resume_text)
                clean_jd = preprocess_text(job_description)

                resume_skills = extract_skills(clean_resume)
                jd_skills = extract_skills(clean_jd)

                matched_skills = get_matching_skills(resume_skills, jd_skills)
                missing_skills = get_missing_skills(resume_skills, jd_skills)

                st.markdown("### skills")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**matched ({len(matched_skills)})**")
                    for s in matched_skills:
                        render_status(True, s)

                with col2:
                    st.markdown(f"**missing ({len(missing_skills)})**")
                    for s in missing_skills:
                        render_status(False, s)

                st.markdown("### bullet point quality")

                quality_sections = ["experience", "projects"]
                any_bullets_checked = False

                for sec_name in quality_sections:
                    if sec_name not in sections:
                        continue

                    bullet_results = analyze_section(sections[sec_name])

                    if not bullet_results:
                        continue

                    any_bullets_checked = True
                    st.markdown(f"**{sec_name}**")

                    for idx, r in enumerate(bullet_results):
                        state_key = f"rewrite_{sec_name}_{idx}"
                        is_flagged = r["weak_verb"] or not r["has_metric"]
                        card_class = "flag" if is_flagged else "ok"

                        # st.markdown(f'<div class="bullet-card {card_class}">', unsafe_allow_html=True)
                        st.markdown(r["text"])

                        if is_flagged:
                            if r["weak_verb"]:
                                suggestion_text = ", ".join(r["suggestions"])
                                st.caption(f'weak phrase: "{r["weak_verb"]}" → try: {suggestion_text}')
                            if not r["has_metric"]:
                                st.caption("no number/metric found — consider quantifying the impact")

                            # show the cached rewrite if we already generated one for this bullet
                            if state_key in st.session_state:
                                st.success(f"✨ {st.session_state[state_key]}")
                            else:
                                if st.button("✨ rewrite this", key=f"btn_{state_key}"):
                                    try:
                                        with st.spinner("rewriting..."):
                                            rewritten = rewrite_bullet(r["text"])
                                        st.session_state[state_key] = rewritten
                                        st.rerun()
                                    except Exception as e:
                                        st.error("Couldn't generate a rewrite right now. Please try again.")
                                        print(f"[Rewrite error] {type(e).__name__}: {e}")

                        # st.markdown('</div>', unsafe_allow_html=True)

                if not any_bullets_checked:
                    st.caption(
                        "No bullet points detected in Experience/Projects "
                        "sections to check (make sure bullets start with "
                        "-, •, or *)."
                    )

            except Exception as e:
                st.error(
                    "Something went wrong while analyzing your resume. "
                    "Please try again, or try a different PDF."
                )
                print(f"[Analysis error] {type(e).__name__}: {e}")

else:
    # empty state shown before any file is uploaded
    st.markdown(
        '<div style="font-family: \'JetBrains Mono\', monospace; color: var(--text-dim); '
        'padding: 3rem 0; text-align: center; border: 1px dashed var(--border); border-radius: 8px;">'
        '↑ upload a resume in the sidebar to begin'
        '</div>',
        unsafe_allow_html=True
    )