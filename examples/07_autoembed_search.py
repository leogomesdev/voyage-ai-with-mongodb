"""Run $vectorSearch with query-time auto-embedding (no client-side query vector)."""

import sys
from pathlib import Path

# Allow `python examples/07_autoembed_search.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.db import get_auto_collection

collection = get_auto_collection()

query = "ancient construction methods"

# Atlas embeds the query text with voyage-4 at query time
results = collection.aggregate(
    [
        {
            "$vectorSearch": {
                "index": "vector_index_auto",
                "path": "description",
                "query": {
                    "text": query,
                },
                "model": "voyage-4",
                "numCandidates": 100,
                "limit": 10,
            }
        }
    ]
)

print(f'Query: "{query}"\n')
for doc in results:
    print(doc.get("title", doc))
