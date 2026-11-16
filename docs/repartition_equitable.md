# Répartition équitable du travail — CyberGuard AI

Les points (1 à 8) sont des estimations de charge, à ajuster ensemble en 10 minutes.
Objectif : charge égale à ±2 points près, domaines cohérents, relecture croisée.

## Must Have (MVP) — 52 points

| ID | Story | Pts | Resp. | Relecteur |
|---|---|---|---|---|
| US-01 | Ingestion reproductible du corpus | 3 | Hela | Yassmine |
| US-02 | Chunking par titres + métadonnées | 5 | Hela | Yassmine |
| US-03 | Indexation Qdrant + BM25 | 5 | Jihen | Hela |
| US-04 | Recherche hybride RRF + baseline | 8 | Hela | Yassmine |
| US-05 | API `POST /ask` | 5 | Yassmine | Jihen |
| US-06 | Sources dans chaque réponse | 3 | Yassmine | Jihen |
| US-07 | Abstention hors corpus | 5 | Yassmine | Jihen |
| US-08 | Interface de chat | 8 | Jihen | Hela |
| US-09a | Rédiger et vérifier les questions du jeu d'évaluation (≥ 80 → ≈ 27 chacun) | 3 (1 chacun) | Hela, Yassmine, Jihen | Rotation |
| US-09b | Pipeline Ragas + rapport vs baseline | 4 | Yassmine | Hela |
| US-10 | Dépôt propre, sans secrets, README | 3 | Jihen | Hela |

## Should Have — 21 points

| ID | Story | Pts | Resp. | Relecteur |
|---|---|---|---|---|
| US-11 | Reranking Cross-Encoder | 5 | Hela | Yassmine |
| US-12 | Filtres par catégorie | 3 | Hela | Yassmine |
| US-13 | Historique des conversations | 3 | Jihen | Hela |
| US-14 | Feedback pouce haut / bas | 2 | Yassmine | Jihen |
| US-15 | Tracing et observabilité | 3 | Yassmine | Jihen |
| US-16 | Docker Compose complet | 5 | Jihen | Hela |

## Totaux

| Membre | Must | Should | Total | Domaine |
|---|---|---|---|---|
| Hela | 17 | 8 | **25** | Données et retrieval |
| Yassmine | 18 | 5 | **23** | Backend, évaluation, MLOps |
| Jihen | 17 | 8 | **25** | Interface, indexation, infra |

Relecture en anneau : Hela relit Jihen, Jihen relit Yassmine, Yassmine relit Hela (sauf indication contraire ci-dessus).

## Rôles transversaux tournants

| Rôle | Séance 1 | Séance 2 | Séance 3 | Séance 4+ |
|---|---|---|---|---|
| Gardien du dépôt Git (merges, `main` propre) | Jihen | Hela | Yassmine | rotation |
| Pitch / démo | Hela | Yassmine | Jihen | rotation |
| Compte rendu et mise à jour des docs | Yassmine | Jihen | Hela | rotation |

## Règle de rééquilibrage

Si une story dépasse son estimation de plus de 50 %, le membre le signale en séance et on déplace une story Should ou Could vers celui qui a de la marge. Les Must restent protégés.
