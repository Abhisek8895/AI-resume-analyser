from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, jd_text):

    if not resume_text.strip() or not jd_text.strip():
        return 0

    try:
        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(similarity * 100, 2)

    except Exception as e:
        print("Similarity Error:", e)
        raise