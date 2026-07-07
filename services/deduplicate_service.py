import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

SIMILARITY_THRESHOLD = 0.85

def deduplicate_articles(news):

    if len(news) <= 1:
        return news

    texts = [
        (
            article.get("title", "")
            + ". "
            + article.get("description", "")
        ).strip()
        for article in news
    ]

    embeddings = model.encode(
        texts,
        batch_size=16,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    unique_articles = []
    unique_embeddings = []
    seen_titles = set()

    for article, embedding in zip(news, embeddings):

        title = article.get("title", "").strip().lower()

        if title in seen_titles:
            continue

        seen_titles.add(title)

        duplicate = False

        for existing in unique_embeddings:

            if np.dot(embedding, existing) >= SIMILARITY_THRESHOLD:
                duplicate = True
                break

        if not duplicate:
            unique_articles.append(article)
            unique_embeddings.append(embedding)

    return unique_articles