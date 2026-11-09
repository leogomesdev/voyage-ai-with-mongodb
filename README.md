# Voyage AI with MongoDB

Examples for Voyage AI embeddings and MongoDB Atlas Vector Search.

- **01–02:** Voyage-only (in-memory; no Atlas Vector Search)
- **03–05:** Bring-your-own embeddings stored in Atlas + `$vectorSearch`
- **06–07:** Atlas **autoEmbed** (MongoDB embeds `description` / query text)
- **08:** Vector search candidates + Voyage reranking (`rerank-2.5`)

## Prerequisites

- Python 3.12+
- A Model API key from [MongoDB Atlas / Voyage AI](https://www.mongodb.com/docs/voyageai/quickstart)
- A MongoDB Atlas cluster with Vector Search
- Atlas **Network Access** that allows your current IP

## Setup

From the project root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set VOYAGE_API_KEY and MONGODB_URI (and DB/collection names if desired)
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `VOYAGE_API_KEY` | Atlas Model API key (`ai.mongodb.com`) |
| `MONGODB_URI` | Atlas SRV connection string |
| `MONGODB_DB` | Database name (default `mydatabase`) |
| `MONGODB_COLLECTION` | Bring-your-own embeddings collection (default `mycollection`) |
| `MONGODB_COLLECTION_AUTO` | autoEmbed collection (default `mycollection_auto`) |

Keep real secrets in `.env` only (gitignored). Commit `.env.example` with placeholders.

## Run the examples

Always run from the project root with the venv activated.

### Voyage-only (in-memory)

```bash
python examples/01_embed_document.py
python examples/02_semantic_search.py
```

### Atlas Vector Search (bring-your-own embeddings)

```bash
# 1) Embed sample docs and insert into MONGODB_COLLECTION
python examples/03_store_embeddings.py

# 2) Create vector_index on the embedding field
python examples/04_create_vector_index.py

# 3) Wait until the index is READY in Atlas (Search Indexes), then search
python examples/05_vector_search.py

# 4) Same retrieval, then rerank candidates with Voyage rerank-2.5
python examples/08_vector_search_and_rerank.py
```

### Atlas autoEmbed

Uses a **separate** collection (`MONGODB_COLLECTION_AUTO`) so it does not clash with the bring-your-own embeddings index.

```bash
# 1) Insert text-only docs + create vector_index_auto on description
python examples/06_seed_and_autoembed_index.py

# 2) Wait until the index is READY, then search (query text embedded by Atlas)
python examples/07_autoembed_search.py
```

If a search returns no results, the index may still be building — wait and re-run.

## Project layout

| Path | Purpose |
|------|---------|
| `requirements.txt` | Libraries (committed) |
| `.env.example` | Env template (committed) |
| `.env` | Real secrets (gitignored) |
| `examples/data.py` | Sample documents |
| `examples/db.py` | Shared Voyage + Mongo clients |
| `examples/01_embed_document.py` | Single-document embedding |
| `examples/02_semantic_search.py` | In-memory semantic search |
| `examples/03_store_embeddings.py` | Embed + insert into Atlas |
| `examples/04_create_vector_index.py` | Bring-your-own embeddings vector search index |
| `examples/05_vector_search.py` | `$vectorSearch` with query vector |
| `examples/06_seed_and_autoembed_index.py` | Seed + autoEmbed index |
| `examples/07_autoembed_search.py` | `$vectorSearch` with auto query embed |
| `examples/08_vector_search_and_rerank.py` | `$vectorSearch` + Voyage `rerank-2.5` |

## Security

- Never commit `.env` or put real passwords/API keys in the README.
- If credentials were shared in chat, rotate the Atlas database user password and Model API key.
