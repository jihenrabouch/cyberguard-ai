import hashlib
import math

from qdrant_client import QdrantClient

from backend.retrieval.hybrid import BM25Index, build_dense_index, hybrid_search, rrf, tokenize

DIM = 64
CHUNKS = [
    {"chunk_id": "pw-1", "text": "Use bcrypt or Argon2 to hash passwords with a salt", "title": "Password Storage", "section": "Hashing", "url": "u1", "source_file": "Password_Storage_Cheat_Sheet.md"},
    {"chunk_id": "sql-1", "text": "Use parameterized queries to prevent SQL injection", "title": "SQL Injection Prevention", "section": "Defenses", "url": "u2", "source_file": "SQL_Injection_Prevention_Cheat_Sheet.md"},
    {"chunk_id": "sess-1", "text": "Regenerate the session identifier after login and set cookie flags", "title": "Session Management", "section": "Cookies", "url": "u3", "source_file": "Session_Management_Cheat_Sheet.md"},
]


def fake_embed(texts):
    """Embedding factice (sac de mots haché) : permet de tester sans télécharger BGE-M3."""
    out = []
    for t in texts:
        v = [0.0] * DIM
        for w in tokenize(t):
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % DIM] += 1.0
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        out.append([x / n for x in v])
    return out


def test_rrf_favorise_les_documents_presents_dans_les_deux_classements():
    a = [{"chunk_id": "x"}, {"chunk_id": "y"}]
    b = [{"chunk_id": "z"}, {"chunk_id": "y"}]
    assert rrf([a, b], top=1)[0]["chunk_id"] == "y"


def test_indexation_nombre_de_points_egal_nombre_de_chunks():
    client = QdrantClient(":memory:")
    assert build_dense_index(client, CHUNKS, fake_embed, size=DIM) == len(CHUNKS)


def test_recherche_hybride_retrouve_le_bon_chunk_avec_ses_metadonnees():
    client = QdrantClient(":memory:")
    build_dense_index(client, CHUNKS, fake_embed, size=DIM)
    res = hybrid_search(client, fake_embed, BM25Index(CHUNKS), "how to prevent SQL injection", top=2)
    assert res[0]["chunk_id"] == "sql-1"
    assert res[0]["title"] and res[0]["section"] and res[0]["url"]
