"""Create a Vector Search index on the bring-your-own `embedding` field."""

import sys
from pathlib import Path

# Allow `python examples/04_create_vector_index.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pymongo.operations import SearchIndexModel

from examples.db import get_collection

collection = get_collection()

# voyage-4 embeddings are 1024-dimensional; use dotProduct (normalized vectors)
search_index_model = SearchIndexModel(
    definition={
        "fields": [
            {
                "numDimensions": 1024,
                "path": "embedding",
                "similarity": "dotProduct",
                "type": "vector",
            }
        ]
    },
    name="vector_index",
    type="vectorSearch",
)

# Idempotent-ish: drop existing index with the same name if present
existing = {idx["name"] for idx in collection.list_search_indexes()}
if "vector_index" in existing:
    collection.drop_search_index("vector_index")
    print("Dropped existing search index: vector_index")

result = collection.create_search_index(model=search_index_model)
print(f"Created vector search index: {result}")
print("Wait until the index status is READY in Atlas before running 05_vector_search.py")
