import numpy as np
from app.embeddings import generate_embedding

cache = []

SIMILARITY_THRESHOLD = 0.80

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

        if similarity >= SIMILARITY_THRESHOLD:
            return item["answer"]

    return None
