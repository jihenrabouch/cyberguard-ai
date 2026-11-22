"""Métriques de retrieval (Recall@k, NDCG@k) sur un jeu de questions annoté.

Format du jeu de questions (JSONL, une question par ligne) :
    {"id": "q001", "question": "Comment stocker les mots de passe ?",
     "expected_files": ["Password_Storage_Cheat_Sheet.md"], "type": "simple"}

- `expected_files` : fiches contenant la réponse (liste vide = question hors corpus,
  exclue des métriques de retrieval et réservée au test d'abstention).
- `type` : simple, synonyme, multi-doc, ambigue ou hors-corpus.

Pertinence : un chunk est pertinent si son `source_file` figure dans `expected_files`
(annotation au niveau de la fiche, plus grossière qu'au niveau de la section).
"""
import json
import math
from collections import Counter


def load_questions(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def recall_at_k(rels, k=5):
    """1 si au moins un passage pertinent figure parmi les k premiers résultats, sinon 0."""
    return 1.0 if any(rels[:k]) else 0.0


def ndcg_at_k(rels, n_relevant, k=5):
    """NDCG@k avec pertinence binaire ; n_relevant = nombre de chunks pertinents dans le corpus."""
    dcg = sum(r / math.log2(i + 2) for i, r in enumerate(rels[:k]))
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(k, n_relevant)))
    return dcg / ideal if ideal else 0.0


def relevant_counts(chunks):
    """Nombre de chunks par fiche source (sert au calcul de l'idéal du NDCG)."""
    return Counter(c["source_file"] for c in chunks)


def evaluate(search_fn, questions, counts, k=5):
    """Évalue un système de recherche.

    search_fn(question) -> liste de chunks (dicts avec `source_file`), classés par pertinence.
    """
    recalls, ndcgs, misses = [], [], []
    by_type = {}
    for q in questions:
        expected = set(q.get("expected_files", []))
        if not expected:
            continue  # hors corpus : évalué ailleurs (abstention)
        results = search_fn(q["question"])[:k]
        rels = [1 if r["source_file"] in expected else 0 for r in results]
        n_rel = sum(counts[f] for f in expected)
        rec, nd = recall_at_k(rels, k), ndcg_at_k(rels, n_rel, k)
        recalls.append(rec)
        ndcgs.append(nd)
        by_type.setdefault(q.get("type", "?"), []).append(rec)
        if not rec:
            misses.append(q["question"])
    n = len(recalls)
    return {
        "n": n,
        f"recall@{k}": sum(recalls) / n if n else 0.0,
        f"ndcg@{k}": sum(ndcgs) / n if n else 0.0,
        "recall_par_type": {t: sum(v) / len(v) for t, v in by_type.items()},
        "echecs": misses,
    }
