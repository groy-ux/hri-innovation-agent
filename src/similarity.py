from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def fit_vectorizer(texts):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    return vectorizer, X


def compute_similarity_matrix(texts):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(X)
    return similarity_matrix


def find_top_k_similar(new_text, existing_texts, titles, k=3):
    vectorizer = TfidfVectorizer()
    X_existing = vectorizer.fit_transform(existing_texts)
    X_new = vectorizer.transform([new_text])

    similarities = cosine_similarity(X_new, X_existing)[0]

    results = []
    for idx, score in enumerate(similarities):
        results.append({
            "title": titles[idx],
            "similarity_score": round(float(score), 3)
        })

    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    return results[:k]


def get_most_similar_pairs(similarity_matrix, titles):
    results = []

    for i in range(len(titles)):
        best_j = None
        best_score = -1

        for j in range(len(titles)):
            if i == j:
                continue
            if similarity_matrix[i][j] > best_score:
                best_score = similarity_matrix[i][j]
                best_j = j

        results.append({
            "idea": titles[i],
            "most_similar_idea": titles[best_j],
            "similarity_score": round(float(best_score), 3)
        })

    return results