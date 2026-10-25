import numpy as np
from app.embeddings import generate_embedding

cache = []

SIMILARITY_THRESHOLD = 0.75


def add_to_cache(question: str, answer: str):
    embedding = generate_embedding(question)

    cache.append({
        "question": question,
        "embedding": embedding,
        "answer": answer
    })


def search_cache(question: str):
    query_embedding = generate_embedding(question)
    best_match = None
    best_similarity = SIMILARITY_THRESHOLD

    for item in cache:
        similarity = np.dot(
            query_embedding, item["embedding"]
        ) / (
            np.linalg.norm(query_embedding)
            * np.linalg.norm(item["embedding"])
        )

        print("Similarity score:", similarity)

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = item

    if best_match is not None:
        return best_match["answer"]

    return None