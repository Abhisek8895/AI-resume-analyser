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