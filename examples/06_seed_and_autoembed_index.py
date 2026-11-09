"""Seed text-only docs and create an autoEmbed Vector Search index."""

import sys
from pathlib import Path

# Allow `python examples/06_seed_and_autoembed_index.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pymongo.operations import SearchIndexModel

from examples.data import data
from examples.db import get_auto_collection

collection = get_auto_collection()

# Text-only copies — Atlas autoEmbed generates vectors from `description`
docs = [
    {
        "title": item["title"],
        "description": item["description"],
        "category": item["category"],
    }
    for item in data
]

collection.delete_many({})
collection.insert_many(docs)
print(f"Inserted {len(docs)} text-only documents into {collection.name}")

# Auto-embedding index: MongoDB embeds `description` with voyage-4 at index time
search_index_model = SearchIndexModel(
    definition={
        "fields": [
            {
                "type": "autoEmbed",
                "modality": "text",
                "path": "description",
                "model": "voyage-4",
            }
        ]
    },
    name="vector_index_auto",
    type="vectorSearch",
)

existing = {idx["name"] for idx in collection.list_search_indexes()}
if "vector_index_auto" in existing:
    collection.drop_search_index("vector_index_auto")
    print("Dropped existing search index: vector_index_auto")

result = collection.create_search_index(model=search_index_model)
print(f"Created autoEmbed vector search index: {result}")
print("Wait until the index status is READY in Atlas before running 07_autoembed_search.py")
