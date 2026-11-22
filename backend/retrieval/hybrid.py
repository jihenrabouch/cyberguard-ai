"""Indexation et recherche hybride (dense Qdrant + BM25) avec fusion RRF.

Contrat d'entrée (fichier JSONL, un chunk par ligne, produit par l'ingestion) :
    {"chunk_id": "Authentication_Cheat_Sheet-0007",
     "text": "...", "title": "Authentication", "section": "Password Storage",
     "url": "https://cheatsheetseries.owasp.org/...", "source_file": "Authentication_Cheat_Sheet.md"}
"""
import json
import pickle
import re

COLLECTION = "owasp_chunks"
EMBED_MODEL = "BAAI/bge-m3"
VECTOR_SIZE = 1024
RRF_K = 60


def load_chunks(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def tokenize(text):
    return re.findall(r"\w+", text.lower())


class BgeM3Embedder:
    """Callable : liste de textes -> liste de vecteurs normalisés (1024 dimensions)."""

    def __init__(self, model_name=EMBED_MODEL):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def __call__(self, texts):
        vecs = self.model.encode(texts, normalize_embeddings=True, batch_size=16, show_progress_bar=False)
        return vecs.tolist()


def build_dense_index(client, chunks, embed, collection=COLLECTION, size=VECTOR_SIZE, batch=32):
    from qdrant_client.models import Distance, PointStruct, VectorParams
    if client.collection_exists(collection):
        client.delete_collection(collection)
    client.create_collection(collection, vectors_config=VectorParams(size=size, distance=Distance.COSINE))
    for i in range(0, len(chunks), batch):
        part = chunks[i:i + batch]
        vecs = embed([c["text"] for c in part])
        points = [PointStruct(id=i + j, vector=v, payload=c) for j, (c, v) in enumerate(zip(part, vecs))]
        client.upsert(collection, points=points)
    return client.count(collection).count


class BM25Index:
    def __init__(self, chunks):
        from rank_bm25 import BM25Okapi
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])

    def search(self, query, k=20):
        scores = self.bm25.get_scores(tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.chunks[i] for i in order if scores[i] > 0]

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)


def dense_search(client, embed, query, k=20, collection=COLLECTION):
    res = client.query_points(collection, query=embed([query])[0], limit=k, with_payload=True)
    return [p.payload for p in res.points]


def rrf(rankings, k=RRF_K, top=10):
    """Reciprocal Rank Fusion : score = somme de 1 / (k + rang) sur chaque classement."""
    scores, docs = {}, {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            cid = doc["chunk_id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
            docs[cid] = doc
    best = sorted(scores, key=scores.get, reverse=True)[:top]
    return [{**docs[c], "rrf_score": scores[c]} for c in best]


def hybrid_search(client, embed, bm25, query, k_candidates=20, top=5, collection=COLLECTION):
    dense = dense_search(client, embed, query, k=k_candidates, collection=collection)
    lexical = bm25.search(query, k=k_candidates)
    return rrf([dense, lexical], top=top)
