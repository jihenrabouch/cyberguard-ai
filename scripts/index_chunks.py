"""Indexe les chunks dans Qdrant (vecteurs BGE-M3) et construit l'index BM25.

Usage (depuis la racine du dépôt, Qdrant lancé avec `docker compose up -d`) :
    python scripts/index_chunks.py --chunks data/processed/chunks.jsonl

Contrôles des critères d'acceptation US-03 : nombre de points Qdrant = nombre de chunks,
indexation en moins de 10 minutes. Le script s'arrête avec une erreur si les chunks sont invalides.
"""
import argparse
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qdrant_client import QdrantClient

from backend.retrieval.hybrid import BgeM3Embedder, BM25Index, build_dense_index, load_chunks

REQUIRED_FIELDS = ("chunk_id", "text", "title", "section", "url", "source_file")
MAX_SECONDS = 600

parser = argparse.ArgumentParser()
parser.add_argument("--chunks", default="data/processed/chunks.jsonl")
parser.add_argument("--qdrant-url", default="http://localhost:6333")
parser.add_argument("--bm25-out", default="data/processed/bm25.pkl")
args = parser.parse_args()

chunks = load_chunks(args.chunks)
print(f"{len(chunks)} chunks chargés")

# Contrôle d'entrée : champs obligatoires et absence de doublons
missing = [c.get("chunk_id", "?") for c in chunks if any(not c.get(f) for f in REQUIRED_FIELDS)]
dups = [cid for cid, n in Counter(c.get("chunk_id") for c in chunks).items() if n > 1]
if missing or dups:
    print(f"ERREUR : {len(missing)} chunk(s) avec champ manquant {missing[:5]}, {len(dups)} chunk_id en double {dups[:5]}")
    sys.exit(1)

start = time.time()
n = build_dense_index(QdrantClient(url=args.qdrant_url), chunks, BgeM3Embedder())
duration = time.time() - start
print(f"Qdrant : {n} points indexés")
Path(args.bm25_out).parent.mkdir(parents=True, exist_ok=True)
BM25Index(chunks).save(args.bm25_out)
print(f"BM25 : index enregistré dans {args.bm25_out}")
print(f"Durée : {duration:.1f} s")

print("Contrôle US-03 : points Qdrant = chunks :", "OK" if n == len(chunks) else f"ÉCHEC ({n} ≠ {len(chunks)})")
print(f"Contrôle US-03 : durée < {MAX_SECONDS} s :", "OK" if duration < MAX_SECONDS else "ÉCHEC")
if n != len(chunks):
    sys.exit(1)
