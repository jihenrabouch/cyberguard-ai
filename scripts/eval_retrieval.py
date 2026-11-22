"""Compare la baseline vectorielle seule à la recherche hybride (BM25 + dense + RRF).

Usage (Qdrant lancé, index déjà construit avec scripts/index_chunks.py) :
    python scripts/eval_retrieval.py --questions data/eval/questions.jsonl
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from qdrant_client import QdrantClient

from backend.retrieval.evaluate import evaluate, load_questions, relevant_counts
from backend.retrieval.hybrid import BgeM3Embedder, BM25Index, dense_search, hybrid_search, load_chunks

parser = argparse.ArgumentParser()
parser.add_argument("--questions", default="data/eval/questions.jsonl")
parser.add_argument("--chunks", default="data/processed/chunks.jsonl")
parser.add_argument("--qdrant-url", default="http://localhost:6333")
parser.add_argument("--bm25", default="data/processed/bm25.pkl")
parser.add_argument("--k", type=int, default=5)
parser.add_argument("--out", default=None, help="fichier JSON de sortie (optionnel)")
args = parser.parse_args()

client, embed = QdrantClient(url=args.qdrant_url), BgeM3Embedder()
bm25 = BM25Index.load(args.bm25)
questions = load_questions(args.questions)
counts = relevant_counts(load_chunks(args.chunks))

systems = {
    "Baseline (dense seul)": lambda q: dense_search(client, embed, q, k=args.k),
    "Hybride (BM25 + dense + RRF)": lambda q: hybrid_search(client, embed, bm25, q, top=args.k),
}
report = {name: evaluate(fn, questions, counts, k=args.k) for name, fn in systems.items()}

k = args.k
print(f"{'Système':32} {'N':>4} {'Recall@'+str(k):>10} {'NDCG@'+str(k):>9}")
for name, r in report.items():
    print(f"{name:32} {r['n']:>4} {r[f'recall@{k}']:>10.3f} {r[f'ndcg@{k}']:>9.3f}")
for name, r in report.items():
    print(f"\n{name} — Recall par type : " + ", ".join(f"{t}={v:.2f}" for t, v in r["recall_par_type"].items()))
    for q in r["echecs"][:5]:
        print(f"   raté : {q}")
if args.out:
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRapport enregistré dans {args.out}")
