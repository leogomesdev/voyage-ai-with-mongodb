"""In-memory semantic search: embed docs + query, rank by cosine/dot similarity."""

import sys
from pathlib import Path

# Allow `python examples/02_semantic_search.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
import numpy as np
import voyageai

from examples.data import data

# Load VOYAGE_API_KEY from .env (MongoDB Atlas Model API key)
load_dotenv()

# Client reads VOYAGE_API_KEY from the environment
vo = voyageai.Client()

# Use document descriptions as the searchable corpus
documents = [item["description"] for item in data]

query = "ancient construction methods"

# Embed documents with input_type="document" for retrieval quality
doc_embeddings = vo.embed(
    texts=documents,
    model="voyage-4",
    input_type="document",
).embeddings

# Embed the query with input_type="query"
query_embedding = vo.embed(
    texts=[query],
    model="voyage-4",
    input_type="query",
).embeddings[0]

# Dot product similarity (voyage embeddings are normalized → cosine similarity)
similarities = np.dot(doc_embeddings, query_embedding)

# Rank highest similarity first
ranked_indices = np.argsort(-similarities)

# Print the top 5 matches
for doc_index in ranked_indices[:5]:
    print(f"Document: {documents[doc_index][:100]}...")
    print(f"Similarity score: {similarities[doc_index]:.4f}\n")
