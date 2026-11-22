"""
Script de Test de Recherche Vectorielle Top-5 avec Scores Cosinus et Filtre (Séance 2)
Compatible avec qdrant-client 1.20+ et serveur Qdrant v1.9.0 via l'API REST /points/search.
"""

import os
import json
import argparse
import logging
from typing import Optional, List
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SearchTest")

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_REST_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "owasp_chunks")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-m3")


class SearchHit:
    """Représente un résultat retourné par Qdrant."""

    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload


def search_qdrant_rest(
    host: str,
    port: int,
    collection: str,
    query_vector: List[float],
    limit: int,
    query_filter: Optional[qmodels.Filter],
) -> List[SearchHit]:
    """Appelle l'endpoint REST /points/search (supporté par Qdrant v1.9.0)."""
    body = {
        "vector": query_vector,
        "limit": limit,
        "with_payload": True,
    }
    if query_filter is not None:
        if hasattr(query_filter, "model_dump"):
            body["filter"] = query_filter.model_dump(exclude_none=True)
        else:
            body["filter"] = query_filter.dict(exclude_none=True)

    url = f"http://{host}:{port}/collections/{collection}/points/search"
    req = urlrequest.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlrequest.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Erreur HTTP Qdrant ({e.code}) sur {url}: {err_body}") from e
    except URLError as e:
        raise RuntimeError(f"Impossible de joindre Qdrant sur {url}: {e.reason}") from e

    hits: List[SearchHit] = []
    for item in data.get("result", []):
        hits.append(
            SearchHit(
                score=float(item.get("score", 0.0)),
                payload=item.get("payload") or {},
            )
        )
    return hits


def run_search(
    query: str,
    top_k: int = 5,
    category: Optional[str] = None,
    collection: str = COLLECTION_NAME,
    host: str = QDRANT_HOST,
    port: int = QDRANT_PORT,
    model_name: str = EMBEDDING_MODEL_NAME,
):
    # Vérification rapide de la connectivité client si besoin
    _ = QdrantClient(host=host, port=port, check_compatibility=False)

    logger.info(f"Chargement du modèle d'embeddings : {model_name}...")
    embedder = SentenceTransformer(model_name)

    logger.info(f"Requête : '{query}' | Filtre category={category or 'AUCUN'} | Top-{top_k}")
    query_vector = embedder.encode(query, normalize_embeddings=True).tolist()

    q_filter: Optional[qmodels.Filter] = None
    if category:
        q_filter = qmodels.Filter(
            must=[
                qmodels.FieldCondition(
                    key="category",
                    match=qmodels.MatchValue(value=category.strip().lower()),
                )
            ]
        )

    results = search_qdrant_rest(
        host=host,
        port=port,
        collection=collection,
        query_vector=query_vector,
        limit=top_k,
        query_filter=q_filter,
    )

    print("\n" + "=" * 80)
    print(f"TOP-{top_k} COSINE | Collection: {collection} | Filtre category: {category or 'Tous'}")
    print("=" * 80)

    if not results:
        print("Aucun résultat trouvé.")
    for rank, hit in enumerate(results, 1):
        p = hit.payload or {}
        print(
            f"\n[Rang {rank}] Score Cosine: {hit.score:.4f} | "
            f"Category: {p.get('category')} | Doc: {p.get('doc_id')} | Page/Section: {p.get('page')}"
        )
        print(f"Source : {p.get('source')}")
        print(f"Extrait: {p.get('content', '')[:250]}")
    print("\n" + "=" * 80)


def parse_args():
    parser = argparse.ArgumentParser(description="Recherche vectorielle Top-5 filtrée dans Qdrant")
    parser.add_argument(
        "--query", "-q",
        default="Comment stocker les mots de passe de manière sécurisée ?",
        help="Question à rechercher",
    )
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Nombre de résultats (défaut: 5)")
    parser.add_argument("--category", "-c", default=None, help="Filtrer par catégorie (ex: password_storage, injection)")
    parser.add_argument("--collection", default=COLLECTION_NAME, help="Nom de la collection Qdrant")
    parser.add_argument("--host", default=QDRANT_HOST, help="Hôte Qdrant")
    parser.add_argument("--port", type=int, default=QDRANT_PORT, help="Port REST Qdrant")
    parser.add_argument("--model", default=EMBEDDING_MODEL_NAME, help="Modèle d'embedding SentenceTransformer")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_search(
        query=args.query,
        top_k=args.top_k,
        category=args.category,
        collection=args.collection,
        host=args.host,
        port=args.port,
        model_name=args.model,
    )