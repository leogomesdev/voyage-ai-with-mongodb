"""Generate Voyage embeddings and store documents in MongoDB Atlas."""

import sys
from pathlib import Path

# Allow `python examples/03_store_embeddings.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.data import data
from examples.db import get_collection, get_voyage_client

vo = get_voyage_client()
collection = get_collection()

# Work on a shallow copy so we do not mutate the shared data module
docs = [dict(item) for item in data]

# Embed descriptions only (document input type for retrieval quality)
texts_to_embed = [item["description"] for item in docs]
result = vo.embed(texts_to_embed, model="voyage-4", input_type="document")

# Attach vectors to each document
for i, item in enumerate(docs):
    item["embedding"] = result.embeddings[i]

# Replace collection contents with the freshly embedded docs
collection.delete_many({})
collection.insert_many(docs)

print(f"Successfully embedded and inserted {len(docs)} documents")
print(f"Sample embedding dimensions: {len(docs[0]['embedding'])}")
