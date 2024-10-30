import numpy as np
from scipy.spatial.distance import cosine
from models import Embeddings

def search_embeddings(query_embedding, threshold=0.3):
    """Search the database for embeddings similar to the query embedding."""
    results = []
    all_embeddings = Embeddings.query.all()
    for embed in all_embeddings:
        score = cosine(query_embedding, embed.embedding)
        if score < threshold:
            results.append(embed.content_id)
    return results
