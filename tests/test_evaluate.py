from backend.retrieval.evaluate import evaluate, ndcg_at_k, recall_at_k, relevant_counts

CHUNKS = [
    {"chunk_id": "a1", "source_file": "A.md"}, {"chunk_id": "a2", "source_file": "A.md"},
    {"chunk_id": "b1", "source_file": "B.md"}, {"chunk_id": "c1", "source_file": "C.md"},
]


def test_recall_at_k():
    assert recall_at_k([0, 0, 1, 0, 0], k=5) == 1.0
    assert recall_at_k([0, 0, 1], k=2) == 0.0


def test_ndcg_parfait_et_degrade():
    assert ndcg_at_k([1, 1], n_relevant=2, k=5) == 1.0
    assert 0 < ndcg_at_k([0, 1], n_relevant=1, k=5) < 1.0


def test_evaluate_ignore_hors_corpus_et_liste_les_echecs():
    questions = [
        {"question": "q1", "expected_files": ["A.md"], "type": "simple"},
        {"question": "q2", "expected_files": ["B.md"], "type": "synonyme"},
        {"question": "q3", "expected_files": [], "type": "hors-corpus"},
    ]
    search = lambda q: [CHUNKS[0]] if q == "q1" else [CHUNKS[3]]  # q2 : mauvaise fiche
    r = evaluate(search, questions, relevant_counts(CHUNKS), k=5)
    assert r["n"] == 2
    assert r["recall@5"] == 0.5
    assert r["echecs"] == ["q2"]
    assert r["recall_par_type"] == {"simple": 1.0, "synonyme": 0.0}
