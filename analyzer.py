from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model for embeddings
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def calculate_similarity(resume_text, jd_text):

    if not resume_text.strip() or not jd_text.strip():
        return 0

    try:
        # Convert text to embeddings
        resume_embedding = model.encode(resume_text)
        jd_embedding = model.encode(jd_text)

        # Calculate cosine similarity
        similarity = cosine_similarity(
            [resume_embedding],
            [jd_embedding]
        )[0][0]

        return round(similarity * 100, 2)

    except Exception as e:
        print("Similarity Error:", e)
        raise

def get_ats_grade(score):
    if score < 40:
        return "Poor"
    elif score < 60:
        return "Average"
    elif score < 75:
        return "Good"
    elif score < 90:
        return "Very Good"
    else:
        return "Excellent"
    
def get_ats_feedback(score):
    if score < 40:
        return "Your resume is not aligned with this job role."
    elif score < 60:
        return "Partial match. Improve skills and projects."
    elif score < 75:
        return "Good match. A few improvements can help."
    elif score < 90:
        return "Strong match. Well aligned with the JD."
    else:
        return "Excellent match. Highly recommended profile."