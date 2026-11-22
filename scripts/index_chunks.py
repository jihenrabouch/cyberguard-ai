"""Indexe les chunks dans Qdrant (vecteurs BGE-M3) et construit l'index BM25.

Usage (depuis la racine du dépôt, Qdrant lancé avec `docker compose up -d`) :
    python scripts/index_chunks.py --chunks data/processed/chunks.jsonl
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qdrant_client import QdrantClient

from backend.retrieval.hybrid import BgeM3Embedder, BM25Index, build_dense_index, load_chunks

parser = argparse.ArgumentParser()
parser.add_argument("--chunks", default="data/processed/chunks.jsonl")
parser.add_argument("--qdrant-url", default="http://localhost:6333")
parser.add_argument("--bm25-out", default="data/processed/bm25.pkl")
args = parser.parse_args()

chunks = load_chunks(args.chunks)
print(f"{len(chunks)} chunks chargés")
start = time.time()
n = build_dense_index(QdrantClient(url=args.qdrant_url), chunks, BgeM3Embedder())
print(f"Qdrant : {n} points indexés")
Path(args.bm25_out).parent.mkdir(parents=True, exist_ok=True)
BM25Index(chunks).save(args.bm25_out)
print(f"BM25 : index enregistré dans {args.bm25_out}")
print(f"Durée : {time.time() - start:.1f} s")
