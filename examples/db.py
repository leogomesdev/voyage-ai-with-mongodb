"""Shared Voyage AI + MongoDB Atlas clients for example scripts."""

import os
from functools import lru_cache

import certifi
from dotenv import load_dotenv
import pymongo
import voyageai

load_dotenv()


@lru_cache(maxsize=1)
def get_voyage_client() -> voyageai.Client:
    """Voyage client; reads VOYAGE_API_KEY from the environment."""
    return voyageai.Client()


@lru_cache(maxsize=1)
def get_mongo_client() -> pymongo.MongoClient:
    """Atlas client from MONGODB_URI (short-lived scripts use default pool)."""
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI is not set. Copy .env.example to .env and fill it in.")
    # Use certifi CA bundle so TLS works on macOS Python installs
    return pymongo.MongoClient(uri, tlsCAFile=certifi.where())


def get_db_name() -> str:
    return os.getenv("MONGODB_DB", "mydatabase")


def get_collection(name: str | None = None) -> pymongo.collection.Collection:
    """Return a collection; default is MONGODB_COLLECTION (bring-your-own embeddings)."""
    collection_name = name or os.getenv("MONGODB_COLLECTION", "mycollection")
    return get_mongo_client()[get_db_name()][collection_name]


def get_auto_collection() -> pymongo.collection.Collection:
    """Collection used for autoEmbed examples (separate from bring-your-own embeddings)."""
    name = os.getenv("MONGODB_COLLECTION_AUTO", "mycollection_auto")
    return get_collection(name)
