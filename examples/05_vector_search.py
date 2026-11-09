"""Embed a query and run Atlas $vectorSearch against stored embeddings."""

import sys
from pathlib import Path

# Allow `python examples/05_vector_search.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.db import get_collection, get_voyage_client

vo = get_voyage_client()
collection = get_collection()

query = "ancient construction methods"

# Query embeddings use input_type="query"
query_embedding = vo.embed(
    [query],
    model="voyage-4",
    input_type="query",
).embeddings[0]

# Approximate nearest-neighbor search over the embedding field
results = collection.aggregate(
    [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 10,
            }
        }
    ]
)

print(f'Query: "{query}"\n')
for doc in results:
    print(doc["title"])
