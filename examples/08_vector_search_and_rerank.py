"""Atlas $vectorSearch candidates, then Voyage rerank-2.5 for final ranking."""

import sys
from pathlib import Path

# Allow `python examples/08_vector_search_and_rerank.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.db import get_collection, get_voyage_client

vo = get_voyage_client()
collection = get_collection()

query = "ancient construction methods"

# Query embedding for vector retrieval
query_embedding = vo.embed(
    [query],
    model="voyage-4",
    input_type="query",
).embeddings[0]

# Retrieve top candidates, projecting fields used for reranking
cursor = collection.aggregate(
    [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 10,
            }
        },
        {
            "$project": {
                "title": 1,
                "description": 1,
                "_id": 0,
            }
        },
    ]
)

results = list(cursor)
documents = [f"{doc['title']} - {doc['description']}" for doc in results]

print(f'Query: "{query}"\n')
print("Vector search order (before rerank):")
for i, doc in enumerate(results, start=1):
    print(f"  {i}. {doc['title']}")

# Rerank candidates with Voyage rerank-2.5
reranking = vo.rerank(query, documents, model="rerank-2.5")

print("\nReranked order (rerank-2.5):")
for i, item in enumerate(reranking.results, start=1):
    # item.document is the string we passed in; relevance_score is model confidence
    title = item.document.split(" - ", 1)[0]
    print(f"  {i}. {title}  (score={item.relevance_score:.4f})")
