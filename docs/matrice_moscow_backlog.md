# Backlog MoSCoW — CyberGuard AI

**Jalon final : Séance 7.** Les User Stories « Must Have » forment le MVP : sans elles, pas de démonstration.

> Règle : si le temps manque, on protège d'abord l'ingestion, la recherche hybride, les citations, l'évaluation et une démo stable.

**Répartition :** la charge est équilibrée en points de complexité (estimation de l'équipe, à réviser en séance), pas seulement en nombre de stories. Chaque story a un responsable et un relecteur.

## Must Have (MVP)

| ID | User Story | Critères d'acceptation (mesurables) | Pts | Resp. | Relecteur |
|---|---|---|---|---|---|
| US-01 | En tant que membre de l'équipe, je veux ingérer le corpus OWASP de façon reproductible pour disposer d'une base de documents propre. | Le script traite 20/20 fiches sans erreur ; commit OWASP figé et noté dans `CORPUS_MANIFEST.md` ; 0 doublon | 3 | Hela | Yassmine |
| US-02 | En tant que système, je veux découper chaque fiche par titres avec métadonnées pour retrouver des passages précis. | Chunks d’environ 600 tokens (chevauchement ≈ 80) ; 100 % des chunks ont titre, section et URL ; aucun bloc de code coupé en deux (contrôle sur 20 chunks) | 5 | Hela | Yassmine |
| US-03 | En tant que système, je veux indexer les chunks en vectoriel et en BM25. | Nombre de points Qdrant = nombre de chunks ; indexation des 20 fiches en moins de 10 min sur un poste de l'équipe | 5 | Jihen | Hela |
| US-04 | En tant que développeur junior, je veux une recherche hybride avec fusion RRF pour trouver la bonne recommandation malgré les synonymes. | Sur le jeu de test, Recall@5 ≥ 0.85 et supérieur à la baseline vectorielle seule | 8 | Hela | Yassmine |
| US-05 | En tant qu'utilisateur, je veux poser ma question via une API pour obtenir une réponse structurée. | Endpoint `POST /ask` renvoyant `answer` et `sources` en JSON ; latence totale p95 ≤ 15 s (modèle local) ; tests API qui passent | 5 | Yassmine | Jihen |
| US-06 | En tant qu'utilisateur, je veux voir les sources de chaque réponse pour pouvoir la vérifier. | 100 % des réponses contiennent au moins une source (titre, section, lien, extrait) ; sources vérifiées manuellement sur 20 réponses | 3 | Yassmine | Jihen |
| US-07 | En tant qu'utilisateur, je veux que le système s'abstienne quand le corpus ne contient pas la réponse. | ≥ 90 % de refus corrects sur 20 questions hors corpus ; message explicite proposant de reformuler | 5 | Yassmine | Jihen |
| US-08 | En tant qu'utilisateur, je veux une interface de chat qui affiche la réponse et ses sources. | Question → réponse + sources affichées en moins de 15 s ; fonctionne sur la dernière version de Chrome | 8 | Jihen | Hela |
| US-09 | En tant qu'équipe, nous voulons évaluer le système avec un jeu de questions pour prouver sa qualité. | ≥ 80 questions annotées ; rapport Ragas avec Faithfulness ≥ 0.85 et Context Recall ≥ 0.80 ; comparaison avec la baseline | 7 | Yassmine (pipeline Ragas et rapport, 4 pts) ; tous (questions, ≈ 27 chacun, 1 pt chacun) | Hela |
| US-10 | En tant qu'équipe, nous voulons un dépôt propre et sans secrets. | `.env` ignoré, `.env.example` présent ; 0 clé API dans l'historique Git ; commits au format Conventional Commits ; README finalisé | 3 | Jihen | Hela |

## Should Have

| ID | User Story | Critère d'acceptation | Pts | Resp. | Relecteur |
|---|---|---|---|---|---|
| US-11 | Reranking par Cross-Encoder | Gain mesuré sur Recall@5 ou NDCG@5 par rapport à l'hybride sans reranker | 5 | Hela | Yassmine |
| US-12 | Filtres par catégorie (API, authentification, injections…) | Le filtre réduit les résultats à la catégorie choisie dans 100 % des tests | 3 | Hela | Yassmine |
| US-13 | Historique des conversations | Les 10 derniers échanges sont conservés et affichés | 3 | Jihen | Hela |
| US-14 | Feedback utilisateur (pouce haut / bas) | Chaque feedback est enregistré avec la question et la réponse | 2 | Yassmine | Jihen |
| US-15 | Tracing et observabilité (latence, tokens) | Latence et tokens visibles pour 100 % des requêtes | 3 | Yassmine | Jihen |
| US-16 | Docker Compose complet | `docker compose up` démarre tous les services en moins de 5 min | 5 | Jihen | Hela |

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

## Équilibre de la charge

| Membre | Must (pts) | Should (pts) | Total | Domaine |
|---|---|---|---|---|
| Hela | 17 | 8 | **25** | Données et retrieval |
| Yassmine | 18 | 5 | **23** | Backend, évaluation, MLOps |
| Jihen | 17 | 8 | **25** | Interface, indexation, infra |

Les points de US-09 sont répartis ainsi : Yassmine 4 + 1, Hela 1, Jihen 1.

**Relecture en anneau :** Hela relit Jihen, Jihen relit Yassmine, Yassmine relit Hela (voir la colonne Relecteur pour les exceptions).

**Rôles transversaux tournants**

| Rôle | Séance 1 | Séance 2 | Séance 3 | Séance 4+ |
|---|---|---|---|---|
| Gardien du dépôt Git (merges, `main` propre) | Jihen | Hela | Yassmine | rotation |
| Pitch / démo | Hela | Yassmine | Jihen | rotation |
| Compte rendu et mise à jour des docs | Yassmine | Jihen | Hela | rotation |

**Règle de rééquilibrage :** si une story dépasse son estimation de plus de 50 %, le membre le signale en séance et une story Should ou Could est déplacée vers celui qui a de la marge. Les Must restent protégés.
