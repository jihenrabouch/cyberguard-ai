"""Teste la recherche hybride en ligne de commande.

Usage : python scripts/search_demo.py "Comment stocker les mots de passe ?"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qdrant_client import QdrantClient

from backend.retrieval.hybrid import BgeM3Embedder, BM25Index, hybrid_search

parser = argparse.ArgumentParser()
parser.add_argument("query")
parser.add_argument("--qdrant-url", default="http://localhost:6333")
parser.add_argument("--bm25", default="data/processed/bm25.pkl")
parser.add_argument("--top", type=int, default=5)
args = parser.parse_args()

results = hybrid_search(QdrantClient(url=args.qdrant_url), BgeM3Embedder(), BM25Index.load(args.bm25), args.query, top=args.top)
for i, r in enumerate(results, 1):
    print(f"{i}. [{r['rrf_score']:.4f}] {r['title']} > {r['section']}\n   {r['url']}\n   {r['text'][:150]}...\n")
