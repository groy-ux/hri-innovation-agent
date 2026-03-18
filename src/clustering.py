from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def cluster_ideas(texts, n_clusters=2):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = model.fit_predict(X)

    return labels, model, vectorizer


def assign_new_idea_cluster(new_text, model, vectorizer):
    X_new = vectorizer.transform([new_text])
    cluster = model.predict(X_new)[0]
    return cluster