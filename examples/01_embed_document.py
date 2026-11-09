"""Generate a vector embedding for a single document with Voyage AI."""

import sys
from pathlib import Path

# Allow `python examples/01_embed_document.py` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
import voyageai

# Load VOYAGE_API_KEY from .env (MongoDB Atlas Model API key)
load_dotenv()

# Client reads VOYAGE_API_KEY from the environment
vo = voyageai.Client()

document = (
    "The Romans perfected the use of arches, vaults, and concrete in their "
    "monumental buildings. The Colosseum and Pantheon showcase their "
    "engineering brilliance and aesthetic vision."
)

# Embed one document; voyage-4 returns a dense float vector
embeddings = vo.embed(document, model="voyage-4").embeddings[0]

print(len(embeddings))

print(embeddings)
