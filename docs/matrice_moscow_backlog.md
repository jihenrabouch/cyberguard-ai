# Backlog MoSCoW — CyberGuard AI

**Jalon final : Séance 7.** Les User Stories « Must Have » forment le MVP : sans elles, pas de démonstration.

> Règle : si le temps manque, on protège d'abord l'ingestion, la recherche hybride, les citations, l'évaluation et une démo stable.

## Must Have (MVP)

| ID | User Story | Critères d'acceptation (mesurables) | Resp. |
|---|---|---|---|
| US-01 | En tant que membre de l'équipe, je veux ingérer le corpus OWASP de façon reproductible pour disposer d'une base de documents propre. | Le script traite 20/20 fiches sans erreur ; commit OWASP figé et noté dans `CORPUS_MANIFEST.md` ; 0 doublon | Hela |
| US-02 | En tant que système, je veux découper chaque fiche par titres avec métadonnées pour retrouver des passages précis. | Chunks d’environ 600 tokens (chevauchement ≈ 80) ; 100 % des chunks ont titre, section et URL ; aucun bloc de code coupé en deux (contrôle sur 20 chunks) | Hela |
| US-03 | En tant que système, je veux indexer les chunks en vectoriel et en BM25. | Nombre de points Qdrant = nombre de chunks ; indexation des 20 fiches en moins de 10 min sur un poste de l'équipe | Hela |
| US-04 | En tant que développeur junior, je veux une recherche hybride avec fusion RRF pour trouver la bonne recommandation malgré les synonymes. | Sur le jeu de test, Recall@5 ≥ 0.85 et supérieur à la baseline vectorielle seule | Hela |
| US-05 | En tant qu'utilisateur, je veux poser ma question via une API pour obtenir une réponse structurée. | Endpoint `POST /ask` renvoyant `answer` et `sources` en JSON ; latence totale p95 ≤ 15 s (modèle local) ; tests API qui passent | Yassmine |
| US-06 | En tant qu'utilisateur, je veux voir les sources de chaque réponse pour pouvoir la vérifier. | 100 % des réponses contiennent au moins une source (titre, section, lien, extrait) ; sources vérifiées manuellement sur 20 réponses | Yassmine |
| US-07 | En tant qu'utilisateur, je veux que le système s'abstienne quand le corpus ne contient pas la réponse. | ≥ 90 % de refus corrects sur 20 questions hors corpus ; message explicite proposant de reformuler | Yassmine |
| US-08 | En tant qu'utilisateur, je veux une interface de chat qui affiche la réponse et ses sources. | Question → réponse + sources affichées en moins de 15 s ; fonctionne sur la dernière version de Chrome | Jihen |
| US-09 | En tant qu'équipe, nous voulons évaluer le système avec un jeu de questions pour prouver sa qualité. | ≥ 80 questions annotées ; rapport Ragas avec Faithfulness ≥ 0.85 et Context Recall ≥ 0.80 ; comparaison avec la baseline | Yassmine |
| US-10 | En tant qu'équipe, nous voulons un dépôt propre et sans secrets. | `.env` ignoré, `.env.example` présent ; 0 clé API dans l'historique Git ; commits au format Conventional Commits ; README finalisé | Jihen |

## Should Have

| ID | User Story | Critère d'acceptation | Resp. |
|---|---|---|---|
| US-11 | Reranking par Cross-Encoder | Gain mesuré sur Recall@5 ou NDCG@5 par rapport à l'hybride sans reranker | Hela |
| US-12 | Filtres par catégorie (API, authentification, injections…) | Le filtre réduit les résultats à la catégorie choisie dans 100 % des tests | Hela |
| US-13 | Historique des conversations | Les 10 derniers échanges sont conservés et affichés | Jihen |
| US-14 | Feedback utilisateur (pouce haut / bas) | Chaque feedback est enregistré avec la question et la réponse | Yassmine |
| US-15 | Tracing et observabilité (latence, tokens) | Latence et tokens visibles pour 100 % des requêtes | Yassmine |
| US-16 | Docker Compose complet | `docker compose up` démarre tous les services en moins de 5 min | Jihen |

## Could Have

| ID | User Story |
|---|---|
| US-17 | Cache Redis des questions fréquentes |
| US-18 | Comparaison de plusieurs fiches dans une même réponse |
| US-19 | Export des réponses |
| US-20 | Interface bilingue FR / EN |

## Won't Have (pour ce MVP)

- Fine-tuning d'un grand LLM
- Scan automatique d'applications ou pentest
- Kubernetes / multi-tenant complexe
- Application mobile native
- Garantie de sécurité ou conformité juridique
